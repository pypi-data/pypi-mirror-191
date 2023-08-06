"""tushare 获取instruments相关数据"""


import tushare as ts
from typing import Any
from vxquant.model.nomalize import to_symbol
from vxutils import to_datetime, logger, vxtime
from vxdataset.mdapi import DataApiBase, DateTimeType, InstrumentType
from vxdataset.mdapi.instruments import vxInstruments
from 

class vxTSStocklist(DataApiBase):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        allstock = vxInstruments("cn_stocks")
        st_stock = vxInstruments("st_stock")
        df = ts.pro_api().stock_basic(
            list_status="L", fields="ts_code, list_date, delist_date"
        )
        for row in df.iterrows():
            allstock.add_instrument(
                to_symbol(row[1]["ts_code"]), to_datetime(row[1]["list_date"])
            ), to_datetime(row[1]["delist_date"])
        logger.info(f"加载以上是股票完成: {df.shape[0]}个")
        
