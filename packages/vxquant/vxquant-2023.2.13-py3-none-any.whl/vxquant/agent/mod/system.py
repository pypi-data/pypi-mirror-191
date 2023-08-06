"""agent 基础操作"""

from vxsched import vxscheduler, vxIntervalTrigger, vxContext
from vxutils import logger, vxtime
from vxquant.model.exchange import vxTrade
from vxutils import vxWrapper


@vxscheduler.event_handler("__init__")
def init_remote_event(context, _) -> None:
    if (not context.settings.publisher) or (not context.settings.subscriber):
        logger.info("未开启接送和发送远端消息事件模式...")
        return

    context.publisher = vxWrapper.init_by_config(context.settings.publisher)
    logger.info(f"设置publisher: {context.publisher}")
    context.subscriber = vxWrapper.init_by_config(context.settings.subscriber)
    logger.info(f"设置subscriber: {context.subscriber}")

    vxscheduler.submit_event(
        "fetch_remote_events",
        trigger=vxIntervalTrigger(1),
    )
    context.has_remote_event = True
    logger.info("开启接送和发送远端消息事件模式...")


@vxscheduler.event_handler("__init__")
def init_before_trade(context, event) -> None:
    if vxtime.today("09:15:00") < vxtime.now() < vxtime.today("15:00:00"):
        vxscheduler.submit_event("before_trade")
        logger.warning("当前为开盘时间，触发一次before_trade。")
    vxscheduler.trigger_events()


@vxscheduler.event_handler("on_broker_order_status")
def system_on_broker_order_status(context, event) -> None:
    if not context.has_remote_event:
        return

    broker_order = event.data
    remote_order = context.remote_orders.get(broker_order.exchange_order_id, None)
    if remote_order is None:
        logger.debug(f"收到一个非远程委托更新exchange_order_id : {broker_order.exchange_order_id}")
        return

    remote_order.filled_volume = broker_order.filled_volume
    remote_order.filled_amount = broker_order.filled_amount
    remote_order.status = broker_order.status
    remote_order.reject_code = broker_order.reject_code
    remote_order.reject_reason = broker_order.reject_reason

    context.publisher("on_order_status", remote_order)
    logger.info(f"[远程] 上报委托更新: {remote_order}")


@vxscheduler.event_handler("on_broker_execution_report")
def system_on_broker_execution_report(context, event) -> None:
    if not context.has_remote_event:
        return

    broker_trade = event.data
    remote_order = context.remote_orders.get(broker_trade.exchange_order_id, None)
    if remote_order is None:
        logger.debug(
            f"收到一个非远程委托成交回报exchange_order_id : {broker_trade.exchange_order_id}"
        )
        return

    remote_trade = vxTrade(broker_trade.message)
    remote_trade.account_id = remote_order.account_id
    remote_trade.order_id = remote_order.order_id

    context.publisher("on_execution_report", remote_trade)
    logger.info(f"[远程] 上报成交回报: {remote_trade}")


@vxscheduler.event_handler("fetch_remote_events")
def system_fetch_remote_events(context, _) -> None:
    if (
        context.has_remote_event is False
        or context.last_subscriber_time + 1 > vxtime.now()
    ):
        return

    list(map(vxscheduler.submit_event, context.subscriber()))
    context.last_subscriber_time = vxtime.now()
    vxscheduler.trigger_events()


@vxscheduler.event_handler("remote_order_batch")
def system_remote_order_batch(context, event) -> None:
    remote_orders = event.data
    batch_orders = context.tdapi.order_batch(*remote_orders)
    for remote_order, batch_order in zip(remote_orders, batch_orders):
        remote_order.exchange_order_id = batch_order.exchange_order_id
        remote_order.status = batch_order.status
        context.remote_orders[remote_order.exchange_order_id] = remote_order


@vxscheduler.event_handler("remote_order_cancel")
def system_remote_order_cancel(context, event) -> None:
    remote_orders = event.data
    context.tdapi.order_cancel(*remote_orders)


@vxscheduler.event_handler("remote_sync")
def system_remote_sync(context, _) -> None:
    if not context.has_remote_event:
        return

    account = context.tdapi.get_account()
    orders = context.tdapi.get_orders()
    trades = context.tdapi.get_execution_reports()
    context.publisher(
        "reply_sync", {"account": account, "orders": orders, "trades": trades}
    )


@vxscheduler.event_handler("on_exit")
def system_on_exit(context, event) -> None:
    configfile = event.data
    config = vxContext()
    config["settings"] = context.settings
    config["params"] = context.params
    config.save_json(configfile)
    logger.info(f"保存最新的配置文件内容:{configfile}")
    vxscheduler.stop()
    logger.warning("=" * 80)
    logger.warning(f"{' 当天交易结束 ':*^80}")
    logger.warning("=" * 80)
