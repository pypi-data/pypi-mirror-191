"""miniQMT 交易接口"""
from typing import Dict, Union, List
from xtquant import xtdata
from xtquant.xttype import StockAccount
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from vxquant.tdapi.base import vxTdAPIBase
from vxquant.model.exchange import vxCashPosition, vxPosition, vxTick, vxOrder, vxTrade
from vxutils import vxtime, logger
from vxquant.model.tools.qmtData import (
    qmtTickConvter,
    qmtOrderConvter,
    qmtPositionConvter,
    qmtTradeConvter,
    qmtCashPositionConvter,
    qmtAccountInfoConvter,
)


class miniQMTCallback(XtQuantTraderCallback):
    def __init__(self):
        self.broker_orders = {}
        self.broker_trades = {}


class vxQMTTdAPI(vxTdAPIBase):
    def __init__(self, miniqmt_path, account_id, account_type="STOCK"):
        super().__init__()
        self._account = StockAccount(account_id, account_type)
        self._trader = XtQuantTrader(miniqmt_path, int(vxtime.now()))
        self._callback = None

        self._trader.start()
        connect_result = self._trader.connect()
        if connect_result != 0:
            raise ConnectionError(f"连接失败: {connect_result}")

    def register_callback(self, callback: miniQMTCallback) -> None:
        self._callback = callback
        self._callback.broker_orders = self.get_orders()
        self._callback.broker_trades = self.get_execution_reports()
        self._trader.register_callback(self._callback)
        logger.info(f"注册callback类: {self._callback}")
        subscribe_result = self._trader.subscribe(self._account)
        if subscribe_result != 0:
            raise ConnectionError(f"订阅失败: {subscribe_result}")
        logger.info(f"订阅交易所回调成功: {subscribe_result}")

    def get_account(self):
        acc_info = self._trader.query_stock_asset(self._account)
        if not acc_info:
            raise ConnectionError(f"无法获取账户信息，请检查连接. {acc_info}")

        positions = self.get_positions()
        fnl = sum(p.fnl for p in positions.values())
        return qmtAccountInfoConvter(acc_info, fnl=fnl)

    def get_positions(
        self, symbol: str = None
    ) -> Dict[str, Union[vxCashPosition, vxPosition]]:
        qmt_positions = self._trader.query_stock_positions(self._account)
        positions = dict(map(lambda x: qmtPositionConvter(x, "symbol"), qmt_positions))
        if symbol:
            return positions.pop(symbol, {})

        acc_info = self._trader.query_stock_asset(self._account)
        if not acc_info:
            raise ConnectionError(f"无法获取账户信息，请检查连接. {acc_info}")
        cash_position = qmtCashPositionConvter(acc_info)
        positions["CNY"] = cash_position
        return positions

    def get_ticks(self, *symbols) -> Dict[str, vxTick]:
        if len(symbols) == 1 and isinstance(symbols[0], list):
            symbols = symbols[0]

        qmt_symbols = [f"{symbol[-6:]}.{symbol[:2]}" for symbol in symbols]
        qmt_ticks = xtdata.get_full_tick(qmt_symbols)
        for k, v in qmt_ticks.items():
            v["symbol"] = k
        return dict(map(lambda x: qmtTickConvter(x, "symbol"), qmt_ticks.values()))

    def get_orders(self) -> Dict[str, vxOrder]:
        qmt_orders = self._trader.query_stock_orders(self._account)
        return dict(
            map(lambda order: qmtOrderConvter(order, "exchange_order_id"), qmt_orders)
        )

    def get_execution_reports(self) -> List[vxTrade]:
        qmt_trades = self._trader.query_stock_trades(self._account)
        return dict(map(lambda x: qmtTradeConvter(x, "trade_id"), qmt_trades))

    def _to_qmt_symbol(self, symbol):
        """将symbol(SHSE.600000) --> QMT的symbol格式(600000.SH)"""
        return f"{symbol[-6:]}.{symbol[:2]}"

    def order_batch(self, *vxorders: List[vxOrder]) -> List[vxOrder]:
        if len(vxorders) == 1 and isinstance(vxorders[0], list):
            vxorders = vxorders[0]

        for vxorder in vxorders:
            exchange_order_id = self._trader.order_stock(
                account=self._account,
                stock_code=self._to_qmt_symbol(vxorder.symbol),
                order_type=23 if vxorder.order_direction.name == "Buy" else 24,
                order_volume=vxorder.volume,
                price_type=11
                if vxorder.order_type.name == "Limit"
                else 42
                if vxorder.symbol[:2] == "SH"
                else 47,
                price=vxorder.price,
                strategy_name=vxorder.algo_order_id,
                order_remark=vxorder.order_id,
            )
            if exchange_order_id < 0:
                vxorder.status = "Rejected"
                continue

            vxorder.exchange_order_id = exchange_order_id
            vxorder.status = "New"
            if self._callback:
                self._callback.broker_orders[exchange_order_id] = vxorder

        return vxorders

    def order_cancel(self, *vxorders: List[vxOrder]):
        if len(vxorders) == 1 and isinstance(vxorders[0], list):
            vxorders = vxorders[0]

        for vxorder in vxorders:
            if not vxorder.exchange_order_id:
                continue

            seq = self._trader.cancel_order_stock(
                self._account, vxorder.exchange_order_id
            )
            if seq <= 0:
                logger.error(
                    f"委托订单:{vxorder.order_id} 撤单失败{vxorder.symbol} {vxorder.order_direction} {vxorder.volume}"
                )
        return

    def stop(self):
        self._trader.stop()
