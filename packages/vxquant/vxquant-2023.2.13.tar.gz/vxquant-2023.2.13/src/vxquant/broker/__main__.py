""" run zmq broker"""

import zmq
import argparse
import pathlib

from itertools import chain
from vxutils import logger
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Lock
from vxquant.broker.utils import init_socket, frontend_reply, backend_publish
from vxutils.zmqsocket import zmq_pipe
from vxsched import vxscheduler, vxContext, vxEvent


_default_broker_config = {
    "settings": {
        "frontend": {
            "addr": "tcp://127.0.0.1:5555",
            "public_key": "",
            "connect_mode": "bind",
        },
        "backend": {
            "addr": "tcp://127.0.0.1:6666",
            "public_key": "",
            "connect_mode": "bind",
        },
        "events": {},
    },
    "params": {},
    "rpc_methods": {},
}


def on_recv_frontend_msgs(context, msgs):
    """处理前端消息

    Arguments:
        context {vxContext} -- context上下文
        msgs {[client_addr, b'',packed_event]} -- 收到前端消息清单

    前端消息: channel 为：__BROKER__/gateway ————> vxscheduler.submit_event(event)
             channel为: __RPC__  ----> vxscheduler.submit
    """
    client_addr, empty, packed_event = msgs
    assert empty == b""
    event = vxEvent.unpack(packed_event)
    logger.debug(f"frontend 收到来自 {client_addr} 消息: {event}")
    if event.channel == "__BROKER__":
        event.reply_to = client_addr
        vxscheduler.submit_event(event)
    elif event.channel == "__RPC__":
        if event.type not in context.rpc_methods:
            frontend_reply(
                context,
                vxEvent(
                    type="__RPC_REPLY__",
                    data=AttributeError(f"不支持的远程调用方法: {event.type}"),
                    channel=client_addr,
                ),
            )
        event.reply_to = client_addr
        event.channel = context.rpc_methods[event.type]
        backend_publish(context, event)
    elif event.type.startswith("_"):
        frontend_reply(
            context,
            vxEvent(
                type="__ACK__",
                data=ValueError(f"not suport event.type({event.type})"),
                channel=client_addr,
            ),
        )
    else:
        event.reply_to = ""
        backend_publish(context, event)
        frontend_reply(context, vxEvent(type="__ACK__", data="OK", channel=client_addr))


def on_recv_backend_msgs(context, msgs):
    try:
        if msgs[0].startswith(b"\x01"):
            vxscheduler.submit_event(
                vxEvent(
                    type="__ON_SUBSCRIBE__",
                    data=msgs[0][1:].decode("ascii"),
                    channel="__BROKER__",
                )
            )
            return

        if msgs[0].startswith(b"\x00"):
            vxscheduler.submit_event(
                vxEvent(
                    type="__ON_UNSUBSCRIBE__",
                    data=msgs[0][1:].decode("ascii"),
                    channel="__BROKER__",
                )
            )
            return

        _, packed_event = msgs
        event = vxEvent.unpack(packed_event)
        if event.channel == "__BROKER__":
            vxscheduler.submit_event(event)
        elif event.channel:
            frontend_reply(context, event)
        else:
            logger.warning(f"收到错误消息: {event}")

    except Exception as e:
        logger.error(f"error: {e}", exc_info=True)


def on_recv_frontend_recver_msgs(context, msgs):
    context.frontend.send_multipart(msgs)


def on_recv_backend_recver_msgs(context, msgs):
    context.backend.send_multipart(msgs)


def run_broker(config: str = "etc/broker.json", mod_path: str = "mod/"):
    if pathlib.Path(config).is_file():
        context = vxContext.load_json(config, _default_broker_config)
        logger.info(f"加载配置文件: {config} 完成")
    else:
        context = vxContext(_default_broker_config)
        logger.info("使用缺省的配置项")

    context.lock = Lock()
    context.rpc_methods = {}

    if pathlib.Path(__file__).parent.joinpath("mod/").is_dir():
        vxscheduler.load_modules(
            pathlib.Path(__file__).parent.joinpath("mod/").as_posix()
        )

    if mod_path and pathlib.Path(mod_path).is_dir():
        vxscheduler.load_modules(mod_path)

    vxscheduler.start(
        context=context, executor=ThreadPoolExecutor(thread_name_prefix="broker")
    )

    poller = zmq.Poller()

    frontend = init_socket(zmq.ROUTER, context.settings.frontend)
    context.frontend = frontend
    recv_msg_handlers = {frontend: on_recv_frontend_msgs}
    poller.register(frontend, zmq.POLLIN)

    backend = init_socket(zmq.XPUB, context.settings.backend)
    context.backend = backend
    recv_msg_handlers[backend] = on_recv_backend_msgs
    poller.register(backend, zmq.POLLIN)

    context.frontend_sender, frontend_recver = zmq_pipe()
    recv_msg_handlers[frontend_recver] = on_recv_frontend_recver_msgs
    poller.register(frontend_recver, zmq.POLLIN)

    context.backend_sender, backend_recver = zmq_pipe()
    recv_msg_handlers[backend_recver] = on_recv_backend_recver_msgs
    poller.register(backend_recver, zmq.POLLIN)

    while vxscheduler.is_alive():
        flags = dict(poller.poll(1000))
        for s in flags:
            try:
                msgs = s.recv_multipart()
                recv_msg_handlers[s](context, msgs)
            except Exception as err:
                logger.error(f"socket ({s}) handler msg ({msgs}) error: {err}")


@vxscheduler.event_handler("__ON_SUBSCRIBE__")
def backend_on_subscribe(context, event) -> None:
    """订阅事件触发"""
    logger.error(f"收到订阅信息: {event.data} =====")
    if event.data.startswith("rpc_"):
        context.backend_queue.put_nowait(
            vxEvent(
                type="__GET_RPCMETHODS__", channel=event.data, reply_to="__BROKER__"
            )
        )


@vxscheduler.event_handler("__ON_UNSUBSCRIBE__")
def backend_on_unsubscribe(context, event) -> None:
    logger.warning(f"取消订阅信息: {event.data}")
    if event.data.startswith("rpc_"):
        context.rpc_methods = {
            method: channel
            for method, channel in context.rpc_methods.items()
            if channel != event.data
        }


def handle_subscribers(context, event) -> None:
    """处理外部获取的消息"""

    # logger.debug(f"开始抓取subscriber ({context.subscribers})中的消息")
    if not context.subscribers:
        return

    events = [subscriber() for subscriber in context.subscribers]
    for event in chain(*events):
        context.event_queue.put_nowait(event)
        logger.info(f"internal: 收到外部event : ({event.type})")

    return


@vxscheduler.event_handler("__GET_RPCMETHODS__")
def frontend_handle_get_rpc_method(context, event):
    """前端或许rpc methods"""
    reply_event = vxEvent(
        type="__GET_RPCMETHODS__",
        data=context.rpc_methods,
        channel=event.reply_to,
    )
    context.frontend_queue.put_nowait(reply_event)


@vxscheduler.event_handler("__RPC_METHODS__")
def backend_on_update_methods(context, event):
    """更新rpc methods"""

    if isinstance(event.data, Exception):
        logger.warning(f"更新rpc methods 错误: {event.data}")
    else:
        logger.warning(f"更新rpc method: {event.data}")
        context.rpc_methods.update(event.data)


@vxscheduler.event_handler("__READY__")
def frontend_ready_event(context, event):
    """处理前端的ready消息"""
    reply_event = vxEvent(
        type="__ACK__",
        data="OK",
        channel=event.reply_to,
    )
    context.frontend_queue.put_nowait(reply_event)
    logger.debug(f"发送frontend 消息: {reply_event}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""broker server""")
    parser.add_argument(
        "-c",
        "--config",
        help="path to config json file",
        default="config.json",
        type=str,
    )
    parser.add_argument("-m", "--mod", help="模块存放目录", default="./mod", type=str)
    parser.add_argument(
        "-v", "--verbose", help="debug 模式", action="store_true", default=False
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel("DEBUG")

    run_broker(args.config, args.mod)
