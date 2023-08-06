import os
import importlib
import contextlib
from pathlib import Path
import time
from queue import Empty
from itertools import chain
from functools import wraps
from collections import defaultdict
from typing import Any, Optional, Union, Callable
from concurrent.futures import ThreadPoolExecutor as Executor, as_completed
from multiprocessing.dummy import Process, Lock
from multiprocessing import Manager

from vxutils import logger, vxWrapper, vxtime
from vxsched.event import vxEvent, vxTrigger, vxEventQueue
from vxsched.context import vxContext
from vxsched.handlers import vxEventHandlers

__all__ = ["vxEngine", "vxengine", "vxscheduler"]

_default_context = {"settings": {}, "params": {}}


class vxEngine:
    """驱动引擎"""

    def __init__(self, context=None, event_queue=None) -> None:
        if context is None:
            context = vxContext()
        self._event_handlers = vxEventHandlers(context=context)

        self._event_queue = event_queue if event_queue is not None else vxEventQueue()
        self._active = False
        self._executor = None
        self._backends = []
        self._futures = []
        self._is_initialized = False

    @property
    def event_handler(self) -> vxEventHandlers:
        """vxEventHandler"""
        return self._event_handlers

    @property
    def context(self) -> vxContext:
        """上下文"""
        return self._event_handlers.context

    @context.setter
    def context(self, other_context) -> None:
        self._event_handlers.context = other_context

    def is_alive(self):
        return self._active

    def initialize(self, **kwargs) -> None:
        if self._is_initialized is True:
            logger.warning("已经初始化，请勿重复初始化")
            return

        executor = kwargs.pop("executor", None)
        if executor is not None:
            self._executor = executor

        context = kwargs.pop("context", None)
        if context:
            self.context = context
            logger.debug(f"更新context内容: {self.context}")

        event_handlers = kwargs.pop("event_handlers", None)
        if event_handlers:
            self._event_handlers = kwargs.pop("event_handlers")

        event_queue = kwargs.pop("event_queue", None)
        if event_queue:
            self._event_queue = kwargs.pop("event_queue")

        self._active = True
        self.submit_event("__init__")
        logger.info(f"{self.__class__.__name__} 触发初始化时间 (__init__) ... ")
        self.trigger_events()
        self._is_initialized = True

    def submit_event(
        self,
        event: Union[str, vxEvent],
        data: Any = "",
        trigger: Optional[vxTrigger] = None,
        priority: float = 10,
        **kwargs,
    ) -> None:
        """发布消息

        Arguments:
            event {Union[str, vxEvent]} -- 要推送消息或消息类型
            data {Any} -- 消息数据信息 (default: {None})
            trigger {Optional[vxTrigger]} -- 消息触发器 (default: {None})
            priority {int} -- 优先级，越小优先级越高 (default: {10})
        """

        if isinstance(event, str):
            send_event = vxEvent(
                type=event,
                data=data,
                trigger=trigger,
                priority=priority,
                **kwargs,
            )

        elif isinstance(event, vxEvent):
            send_event = event
        else:
            raise ValueError(f"event 类型{type(event)}错误，请检查: {event}")

        logger.debug(f"提交消息: {send_event}")
        self._event_queue.put_nowait(send_event)
        if not self._active:
            logger.warning(
                f"{self.__class__.__name__}(id-{id(self)})"
                f" 未激活，event({send_event.type})将在激活后运行。"
            )

    def trigger_events(self) -> None:
        events = defaultdict(list)
        with contextlib.suppress(Empty):
            while not self._event_queue.empty():
                event = self._event_queue.get_nowait()
                events[event.type].append(event)
        list(map(self.event_handler.trigger, map(max, events.values())))

    def run(self) -> None:
        logger.info(f"{self.__class__.__name__} worker 启动...")
        try:
            while self.is_alive():
                try:
                    event = self._event_queue.get(timeout=1)
                    logger.debug(f"{self.__class__.__name__} 触发 {event.type} 事件...")
                    self.event_handler.trigger(event)
                except Empty:
                    pass
                except Exception as e:
                    logger.info(f"trigger event{event} error: {e}", exc_info=True)

        finally:
            logger.info(f"{self.__class__.__name__} worker 结束...")
            self.stop()

    def serve_forever(self) -> None:
        """运行"""

        self.start()
        list(as_completed(self._futures))
        self.stop()

    def start(self) -> None:
        """开始运行vxScheduler

        Keyword Arguments:
            worker_cnt {int} -- worker个数 (default: {5})
        """

        # if not self.is_alive():
        #    self.initialize()

        logger.info("=" * 60)
        logger.info("=" * 60)
        logger.info("=" * 60)

        if self._executor is None:
            self._executor = Executor(
                thread_name_prefix=f"{self.__class__.__name__}",
            )
            logger.info(
                f"executor 初始化{self._executor},max_workers ="
                f" {self._executor._max_workers}"
            )

        if self._is_initialized is False:
            self.initialize()

        self._futures.extend([self._executor.submit(self.run) for _ in range(5)])
        if self._backends:
            self._futures.extend(
                [
                    self._executor.submit(target, engine=self)
                    for target in self._backends
                ]
            )

    def stop(self) -> None:
        if self._active is False:
            return
        self._active = False

    @classmethod
    def load_modules(cls, mod_path: Union[str, Path]) -> Any:
        """加载策略目录"""
        if not os.path.exists(mod_path):
            logger.warning(msg=f"{mod_path} is not exists")
            return

        modules = os.listdir(mod_path)
        logger.info(f"loading strategy dir: {mod_path}.")
        logger.info("=" * 80)
        for mod in modules:
            if (not mod.startswith("__")) and mod.endswith(".py"):
                try:
                    loader = importlib.machinery.SourceFileLoader(
                        mod, os.path.join(mod_path, mod)
                    )
                    spec = importlib.util.spec_from_loader(loader.name, loader)
                    strategy_mod = importlib.util.module_from_spec(spec)
                    loader.exec_module(strategy_mod)
                    logger.info(f"Load Module: {strategy_mod} Sucess.")
                    logger.info("+" * 80)
                except Exception as err:
                    logger.error(f"Load Module: {mod} Failed. {err}", exc_info=True)
                    logger.error("-" * 80)

    def load_handlers(self, **handlers):
        for event_type, handler in handlers.items():
            self.event_handler(event_type)(handler)

    def backend(self, target: Callable):
        """添加backend 函数
        @engine.backend
        def run_backend(engine):
            pass

        """

        @wraps(target)
        def wrapper_target(engine: vxEngine):
            if not engine.is_alive():
                logger.warning(f"{engine}未进行初始化...")
                return

            logger.info(f"{self.__class__.__name__} backend( {target.__name__} ) 开始运行")
            try:
                return target(engine)
            except Exception as err:
                logger.info(f"{target} 运行错误: {err}", exc_info=True)
            finally:
                logger.info(
                    f"{self.__class__.__name__} backend( {target.__name__} ) 停止运行....",
                    exc_info=True,
                )

        self._backends.append(wrapper_target)
        return target


vxengine = vxEngine()


class vxScheduler:
    def __init__(self):
        self._context = None
        self._executor = None
        self._map_func = map
        self._queue = vxEventQueue()
        self._handlers = defaultdict(set)
        self._active = False
        self._is_initialized = False
        self._worker_threads = []

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id-{id(self)})"

    __repr__ = __str__

    @property
    def context(self):
        return self._context

    def initialize(
        self,
        context: vxContext = None,
        executor: Executor = None,
    ) -> None:
        if self._is_initialized is True:
            logger.warning("已经初始化，请勿重复初始化")
            return

        self._executor = executor
        self._map_func = executor.map if hasattr(executor, "map") else map

        self._context = context or self._context or vxContext(_default_context)
        if context is not None:
            self._context = context
            logger.debug(f"更新context内容: {self.context}")
        elif self._context is None:
            self._context = vxContext(_default_context)
            logger.debug(f"创建缺省context内容: {self.context}")

        self.submit_event("__init__")
        self.trigger_events()
        self._is_initialized = True
        logger.info(f"{self} 触发初始化完成 ... ")

    def is_alive(self):
        """是否运行中"""
        return self._active

    def trigger_events(self, *trigger_events) -> None:
        """同步触发已到期的消息"""
        if len(trigger_events) == 1 and isinstance(trigger_events[0], list):
            trigger_events = trigger_events[0]

        events = defaultdict(list)
        for t_event in trigger_events:
            events[t_event.type].append(t_event)

        with contextlib.suppress(Empty):
            while not self._queue.empty():
                event = self._queue.get_nowait()
                events[event.type].append(event)

        handlers = chain.from_iterable(
            self._handlers[event.type]
            for event in map(max, events.values())
            if self._handlers[event.type]
        )

        results = self._map_func(
            lambda handler: self._run_handler(event=event, handler=handler),
            handlers,
        )
        return list(results)

    def submit_event(
        self,
        event: Union[vxEvent, str],
        data: Any = None,
        trigger: vxTrigger = None,
        priority: float = 10,
        **kwargs,
    ) -> vxEvent:
        """提交一个消息"""

        if isinstance(event, str):
            send_event = vxEvent(
                type=event,
                data=data,
                trigger=trigger,
                priority=priority,
                **kwargs,
            )

        elif isinstance(event, vxEvent):
            send_event = event
        else:
            raise ValueError(f"{self} event 类型{type(event)}错误，请检查: {event}")

        logger.debug(f"提交消息: {send_event}")
        self._queue.put_nowait(send_event)

    def _run_handler(self, handler: Callable, event: vxEvent) -> None:
        """单独运行一个handler"""

        try:
            if handler.lock is not None:
                handler.lock.acquire()

            start = time.perf_counter()
            ret = handler(self.context, event)
        except KeyboardInterrupt:
            ret = None
            logger.warning("用户提前终止... ")

        except Exception as err:
            ret = err
            logger.error(f"{self} run handler error: {err}", exc_info=True)

        finally:
            cost_time = time.perf_counter() - start
            if cost_time > getattr(handler, "time_limit", 1.0):
                logger.warning(
                    f"{self} {handler} 运行时间 {cost_time*1000:,.2f}s.  触发消息: {event}"
                )
            if handler.lock is not None:
                handler.lock.release()

            if (
                event.type != "__handle_timerecord__"
                and self._handlers["__handle_timerecord__"]
            ):
                self.submit_event(
                    "__handle_timerecord__", (str(handler), event, cost_time)
                )

            if event.reply_to and self._handlers["__handle_reply__"]:
                self.submit_event("__handle_reply__", (event, ret))

        return ret

    def register(
        self,
        event_type: str,
        time_limit: float = 1.0,
        lock: Lock = None,
        handler: Callable = None,
    ) -> Callable:
        """注册一个handler"""

        if handler in self._handlers[event_type]:
            return

        setattr(handler, "time_limit", time_limit)
        setattr(handler, "lock", lock)
        self._handlers[event_type].add(handler)
        logger.info(
            f"{self} register event_type:"
            f" '{event_type}' time_limit: {time_limit*1000:,.2f}ms handler: {handler} "
        )

    def unregister(self, event_type: str, handler: Callable) -> None:
        """取消注册handler"""
        if handler in self._handlers[event_type]:
            self._handlers[event_type].remove(handler)
            logger.warning(
                f"{self} unregister event_type: {event_type} handler: {handler}"
            )

    def event_handler(
        self, event_type: str, time_limit: float = 1.0, lock: Lock = None
    ) -> Callable:
        """消息处理函数装饰器"""

        def deco(handler):
            self.register(event_type, time_limit, lock, handler=handler)
            return handler

        return deco

    def run(
        self,
        context: vxContext = None,
        executor: Executor = None,
    ) -> None:
        if self._is_initialized is False:
            self.initialize(context, executor)

        self._active = True

        self._run()

    def _run(self) -> None:
        """单个线程运行"""
        logger.info(f"{self} worker 开始运行...")
        try:
            while self._active:
                with contextlib.suppress(Empty):
                    event = self._queue.get(timeout=1.0)

                    if not self._handlers[event.type]:
                        continue

                    if self._executor:
                        [
                            self._executor.submit(
                                self._run_handler, handler=handler, event=event
                            )
                            for handler in self._handlers[event.type]
                        ]
                    else:
                        [
                            self._run_handler(handler, event)
                            for handler in self._handlers[event.type]
                        ]
        finally:
            self._active = False
            logger.info(f"{self} worker 结束运行...")

    def start(
        self,
        context: vxContext = None,
        executor: Executor = None,
    ) -> None:
        """启动调度器"""
        if self._active:
            logger.info(f"{self} 已经激活运行...")
            return

        if self._is_initialized is False:
            self.initialize(context, executor)

        self._active = True
        self._worker_threads = []
        for i in range(5):
            t = Process(target=self._run, name=f"vxSchedWorker{i}")
            t.daemon = True
            t.start()
            self._worker_threads.append(t)

    def stop(self) -> None:
        """停止调度器"""
        self._active = False
        for t in self._worker_threads:
            if t.is_alive():
                t.join()

    def server_forever(
        self, config: Union[str, Path] = None, mod: Union[str, Path] = "mod/"
    ):
        if isinstance(config, str):
            config = Path(config)

        context = (
            vxContext.load_json(config.absolute(), _default_context)
            if config.exists()
            else vxContext(_default_context)
        )
        executor_settings = context.settings.get("executor", None)
        if executor_settings is not None:
            executor = vxWrapper.init_by_config(context.setting)
        else:
            executor = Executor(thread_name_prefix="vxSchedThread")
        self.load_modules(mod)
        # self.initialize(context, executor=executor)
        self.run(context=context, executor=executor)
        while True:
            vxtime.sleep(1)

    def load_modules(self, mod_path: Union[str, Path]) -> Any:
        """加载策略目录"""
        if isinstance(mod_path, Path):
            mod_path = mod_path.absolute()

        if not os.path.exists(mod_path):
            logger.warning(msg=f"{mod_path} is not exists")
            return

        modules = os.listdir(mod_path)
        logger.info(f"loading strategy dir: {mod_path}.")
        logger.info("=" * 80)
        for mod in modules:
            if (not mod.startswith("__")) and mod.endswith(".py"):
                try:
                    loader = importlib.machinery.SourceFileLoader(
                        mod, os.path.join(mod_path, mod)
                    )
                    spec = importlib.util.spec_from_loader(loader.name, loader)
                    strategy_mod = importlib.util.module_from_spec(spec)
                    loader.exec_module(strategy_mod)
                    logger.info(f"Load Module: {strategy_mod} Sucess.")
                    logger.info("+" * 80)
                except Exception as err:
                    logger.error(f"Load Module: {mod} Failed. {err}", exc_info=True)
                    logger.error("-" * 80)


vxscheduler = vxScheduler()


if __name__ == "__main__":

    class test:
        def __call__(self, *args: Any, **kwds: Any) -> Any:
            time.sleep(2)
            logger.info("this is test")

    s = vxScheduler()
    # s.start(executor=Executor())

    @s.event_handler("test", 10)
    def test2(*args: Any, **kwds: Any):
        time.sleep(1)
        logger.info("this is test2")

    @s.event_handler("__handle_timerecord__")
    def test3(context, event):
        logger.info(f"{event.type}")
        logger.info(event.data)

    s.register("test", 3, handler=test())
    s.register("test1", 3, handler=test())
    s.register("test", 3, handler=test())

    # print(s._handlers)
    s.submit_event("test")
    print("=" * 60)

    print("=" * 60)
    print(s)
    print("=" * 60)
    # s.trigger_events()
    time.sleep(4)
    s.server_forever("config.json")
    s.stop()
