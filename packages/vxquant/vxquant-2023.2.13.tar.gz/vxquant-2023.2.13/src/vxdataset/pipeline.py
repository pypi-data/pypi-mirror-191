"""因子处理流水线"""

import datetime
import tushare as ts
import polars as pl
from abc import abstractmethod
from pathlib import Path
from typing import List, Any, Union
from vxutils import to_datetime

DateTimeType = Union[str, float, datetime.datetime, datetime.date, datetime.timedelta]


class vxDataLoader:
    @abstractmethod
    def get_stock_list(
        self,
        symbols: List[str] = None,
        start_date: DateTimeType = "2005-01-01",
        end_date: DateTimeType = None,
    ):
        """获取股票列表

        Arguments:
            symbols {List[str]} -- 证券代码列表，不提供时，表示全部获取
            start_date {str} -- 起始日期
            end_date {str} -- 终止日期
        """
        pass

    def get_trading_dates(
        start_date: DateTimeType, end_date: DateTimeType, market="cn"
    ) -> List[DateTimeType]:
        """获取交易日历

        Arguments:
            start_date {DateTimeType} -- 开始时间
            end_date {DateTimeType} -- 结束时间

        Keyword Arguments:
            market {str} -- 市场信息，默认:cn  (default: {"cn"})

        Returns:
            List[DateTimeType] -- 返回日期列表: [datetime(2020,1,1,0,0,0), datetime(2020,1,2,0,0,0), ...]
        """
        raise NotImplementedError


class vxTushareDataLoader(vxDataLoader):
    def __init__(self, ts_token: str = "") -> None:
        super().__init__()
        self._pro = ts.pro_api(ts_token)

    def get_stock_list(
        self,
        symbols: List[str] = None,
        start_date: str = "2005-01-01",
        end_date: str = None,
    ):
        pass

    def get_trading_dates(
        self, start_date: DateTimeType, end_date: DateTimeType, market="cn"
    ) -> List[DateTimeType]:
        df = pl.from_pandas(self._pro.trade_cal())
        return (
            df.with_columns([pl.col("con_date").apply(to_datetime).alias("date")])
            .filter(
                (pl.col("date") >= to_datetime(start_date))
                & (pl.col("date") <= to_datetime(end_date))
                & (pl.col("is_open") == 1)
            )
            .sort(by="date")["date"]
        )


class vxFPipeline:
    def __init__(self, loader):
        self._loader = loader
        self._symbol_df = pl.DataFrame([], columns=["symbol", "start_date", "end_date"])

    def instruments(
        self,
        symbols=None,
        start_date: str = None,
        end_date: str = None,
        sec_type: str = "STOCK",
    ) -> "vxFPipeline":
        """通过loader.instrument(symbols)下载相应的symbol,start_date, end_date"""
        self._loader.get_stock_info(symbols, start_date, end_date)
