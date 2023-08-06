"""miniQMT 交易接口"""
import os
import argparse
import pathlib
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from vxquant.tdapi.miniqmt import miniQMTCallback
from vxquant.model.tools.qmtData import qmtOrderConvter, qmtTradeConvter
from vxquant.model.contants import OrderStatus, TradeStatus
from vxquant.model.preset import vxMarketPreset
from vxsched import vxEngine, vxContext, vxDailyTrigger, vxscheduler
from vxutils import vxtime, logger, vxWrapper


_default_qmtagent_config = {
    "settings": {
        "tdapi": {
            "class": "vxquant.tdapi.minqmt.vxQMTTdAPI",
            "params": {"miniqmt_path": "", "account_id": "", "account_type": "NORMAL"},
        },
        "events": {
            "before_trade": "09:15:00",
            "on_trade": "09:30:00",
            "noon_break_start": "11:30:00",
            "noon_break_end": "13:00:00",
            "before_close": "14:45:00",
            "on_close": "14:55:00",
            "after_close": "15:30:00",
            "on_exit": "16:30:00",
        },
        "publisher": {},
        "subscriber": {},
    },
    "params": {},
    "remote_orders": {},
    "last_subscriber_time": 0,
    "has_remote_event": False,
    "publisher": "",
    "subscriber": "",
}


class QMTAccountStatus(Enum):
    INVALID = -1
    OK = 0
    WAITING_LOGIN = 1
    STATUSING = 2
    FAIL = 3
    INITING = 4
    CORRECTING = 5
    CLOSED = 6
    ASSIS_FAIL = 7
    DISABLEBYSYS = 8
    DISABLEBYUSER = 9


class miniQMTAgentCallback(miniQMTCallback):
    def __init__(self, engine: vxEngine) -> None:
        super().__init__()
        self._engine = engine

    def on_connected(self):
        """
        连接成功推送
        """
        logger.info("连接成功")

    def on_disconnected(self):
        """
        连接状态回调
        :return:
        """
        logger.warning("连接断开")

    def on_account_status(self, status):
        """
        账号状态信息推送
        :param response: XtAccountStatus 对象
        :return:
        """
        logger.info(
            "账户状态变更为:"
            f" {status.account_id} {status.account_type} {QMTAccountStatus(status.status)}"
        )

    def on_stock_asset(self, asset):
        """
        资金信息推送
        :param asset: XtAsset对象
        :return:
        """
        logger.info(
            f"on asset callback {asset.account_id}, {asset.cash}, {asset.total_asset}"
        )

    def on_stock_order(self, order):
        """
        委托信息推送
        :param order: XtOrder对象
        :return:
        """
        logger.debug(
            f"收到成交更新: {order.stock_code} {order.order_status} {order.order_sysid}"
        )
        vxorder = qmtOrderConvter(order)

        if vxorder.exchange_order_id not in self.broker_orders:
            self.broker_orders[vxorder.exchange_order_id] = vxorder
            logger.info(f"[新增] 委托订单{vxorder.exchange_order_id} 更新为: {vxorder}")
            self._engine.submit_event("on_broker_order_status", vxorder)
            self._engine.trigger_events()
            return

        broker_order = self.broker_orders[vxorder.exchange_order_id]
        if broker_order.status in [
            OrderStatus.Filled,
            OrderStatus.Expired,
            OrderStatus.Rejected,
            OrderStatus.Canceled,
            OrderStatus.Suspended,
        ]:
            logger.debug(
                f"[忽略更新] 委托订单 {vxorder.exchange_order_id} "
                f" 当前状态:{broker_order.status} 须更新状态: {vxorder.status}"
            )
            return

        if broker_order.filled_volume > vxorder.filled_volume:
            logger.debug(
                f"[忽略更新] 委托订单 {vxorder.exchange_order_id} 当前已成交:"
                f" {broker_order.filled_volume} > 更新状态:{vxorder.filled_volume}"
            )
            return

        # 更新委托订单状态
        broker_order.status = vxorder.status
        broker_order.filled_volume = vxorder.filled_volume
        broker_order.filled_amount = vxorder.filled_amount
        broker_order.updated_dt = vxorder.updated_dt
        self.broker_orders[broker_order.exchange_order_id] = broker_order
        logger.info(f"[更新] 委托订单{vxorder.exchange_order_id} 更新为: {broker_order}")
        self._engine.submit_event("on_broker_order_status", broker_order)
        self._engine.trigger_events()

    def on_stock_trade(self, trade):
        """
        成交信息推送
        :param trade: XtTrade对象
        :return:
        """
        logger.debug(
            f"收到成交信息: {trade.account_id}, {trade.stock_code}, {trade.order_id}"
        )
        vxtrade = qmtTradeConvter(trade)
        if vxtrade.trade_id in self.broker_trades:
            logger.warning("收到重复的委托订单信息")
            return

        if vxtrade.status != TradeStatus.Trade:
            logger.warning(f"收到非成交的回报信息: {vxtrade}")
            return

        if vxtrade.commission == 0:
            _preset = vxMarketPreset(vxtrade.symbol)
            vxtrade.commission = max(
                (
                    vxtrade.price
                    * vxtrade.volume
                    * (
                        _preset.commission_coeff_peramount
                        if vxtrade.order_direction.name == "Buy"
                        else (
                            _preset.commission_coeff_peramount
                            + _preset.tax_coeff_peramount
                        )
                    )
                ),
                5,
            )

        self.broker_trades[vxtrade.trade_id] = vxtrade
        logger.info(f"收到成交回报信息: {vxtrade}")
        self._engine.submit_event("on_broker_execution_report", vxtrade)
        self._engine.trigger_events()

    def on_stock_position(self, position):
        """
        持仓信息推送
        :param position: XtPosition对象
        :return:
        """
        logger.info(f"持仓信息推送: {position.stock_code}, {position.volume}")

    def on_order_error(self, order_error):
        """
        下单失败信息推送
        :param order_error:XtOrderError 对象
        :return:
        """

        if order_error.order_id not in self.broker_orders:
            logger.warning(
                f"下单失败: {order_error.order_id}, {order_error.error_id},"
                f" {order_error.error_msg}"
            )
            return

        broker_order = self.broker_orders[order_error.order_id]
        if broker_order.status in [
            OrderStatus.Filled,
            OrderStatus.Expired,
            OrderStatus.Rejected,
            OrderStatus.Canceled,
            OrderStatus.Suspended,
        ]:
            logger.debug(
                f"[忽略更新] 委托订单 {order_error.exchange_order_id} "
                f" 当前状态:{broker_order.status} 须更新状态: {order_error.error_msg}"
            )
            return

        broker_order.status = "Rejected"
        broker_order.reject_code = "UnknownOrder"
        broker_order.reject_reason = order_error.error_msg
        self._engine.submit_event("on_broker_order_status", broker_order)
        self._engine.trigger_events()


def run_qmtagent(config: str, mod_path: str = "mod/") -> None:
    context = vxContext.load_json(config, _default_qmtagent_config)
    context.configfile = config
    if context.settings.tdapi:
        context.tdapi = vxWrapper.init_by_config(context.settings.tdapi)
        account_info = context.tdapi.get_account()
        logger.info(
            f"[测试下单接口] 账号 {account_info.account_id} 总资产：{account_info.nav:,.2f}元"
        )
        callback = miniQMTAgentCallback(vxscheduler)
        context.tdapi.register_callback(callback)
    else:
        context.tdapi = None

    if pathlib.Path(__file__).parent.joinpath("mod/").is_dir():
        vxscheduler.load_modules(
            pathlib.Path(__file__).parent.joinpath("mod/").as_posix()
        )

    if mod_path and pathlib.Path(mod_path).is_dir():
        vxscheduler.load_modules(mod_path)

    for event_type, run_time in context.settings["events"].items():
        vxscheduler.submit_event(
            event=event_type, trigger=vxDailyTrigger(run_time=run_time)
        )
        logger.info(f"订阅事件{event_type} 触发时间: {run_time}")

    vxscheduler.submit_event("on_exit", data=config, trigger=vxDailyTrigger("16:30:00"))

    logger.info("=" * 80)
    logger.info(f"{' 初始化完成 ':=^80}")
    logger.info("=" * 80)

    try:
        vxscheduler.start(
            context=context,
            executor=ThreadPoolExecutor(thread_name_prefix="workerpool"),
        )
        while vxscheduler.is_alive():
            vxtime.sleep(1)
    finally:
        context.tdapi.stop()
        logger.warning("=" * 80)
        logger.warning(f"{' 当天交易结束 ':*^80}")
        logger.warning("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""miniqmt agent server""")
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

    run_qmtagent(args.config, args.mod)
