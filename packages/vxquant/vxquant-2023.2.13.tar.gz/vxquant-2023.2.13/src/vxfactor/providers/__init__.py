"""供应接口"""


import polars as pl
from abc import ABC, abstractmethod
from typing import Dict, List, Union
from pathlib import Path
from itertools import product
from vxfactor.instruments import vxInstruments
from vxfactor.constants import DateTimeType, InstrumentType
from vxquant.model.exchange import vxTick
from vxutils import vxtime, vxLRUCache, to_datetime, diskcache, DiskCacheUnit


class vxHQProvider(ABC):
    _tickcache = vxLRUCache(100, 3)

    def __call__(self, *symbols: List[InstrumentType]) -> Dict[InstrumentType, vxTick]:
        """实时行情接口

        Returns:
            Dict[InstrumentType, vxTick] -- _description_
        """ """"""
        if len(symbols) == 1 and isinstance(symbols[0], list):
            symbols = symbols[0]

        ticks = {}
        _missing_symbols = []
        for symbol in symbols:
            if symbol in self._tickcache:
                ticks[symbol] = self._tickcache[symbol]
            else:
                _missing_symbols.append(symbol)

        if _missing_symbols:
            ticks = self._hq(_missing_symbols)
            self._tickcache.update(**ticks)

        return {
            symbol: self._tickcache[symbol]
            for symbol in symbols
            if symbol in self._tickcache
        }

    @abstractmethod
    def _hq(self, *symbols: List[InstrumentType]) -> Dict[InstrumentType, vxTick]:
        """实时数据接口

        Returns:
            Dict[InstrumentType, vxTick] -- 返回值样例:
            {
                "SHSE.600000": vxTick(...),
                "SHSE.600001": vxTick(...),
                ...
            }
        """
        pass


class vxCalendarProvider(ABC):
    def __call__(
        self,
        start_date: DateTimeType = None,
        end_date: DateTimeType = None,
        market: str = "cn",
    ):
        start_date = to_datetime(start_date or "2010-01-01")
        end_date = to_datetime(end_date or vxtime.today())

        if f"calendar_{market}" not in diskcache:
            dates = self.get_trade_dates(market)
            diskcache[f"calendar_{market}"] = DiskCacheUnit(
                f"calendar_{market}", dates, to_datetime(dates[-1])
            )
        trade_days = diskcache[f"calendar_{market}"]

        return (
            pl.DataFrame({"trade_date": trade_days})
            .with_columns([pl.col("trade_date").apply(to_datetime)])
            .filter(
                (
                    (pl.col("trade_date") >= start_date)
                    & (pl.col("trade_date") <= end_date)
                )
            )
            .sort(by="trade_date")["trade_date"]
        )

    def get_trade_dates(self, market: str = "cn") -> List[InstrumentType]:
        """获取该市场全部日历

        Arguments:
            market {str} -- 市场代码

        Returns:
            List[InstrumentType] -- 返回值: ['2022-01-01', '2022-01-02', ...]
        """


class vxInstrumentsProvider(ABC):
    def __init__(self, inst_path=".data/instruments") -> None:
        self._inst_path = inst_path

    def __call__(self, instruments_name: str = "allstocks") -> vxInstruments:
        instruments_file = Path(self._inst_path, f"{instruments_name}.parquet")

        inst_records = (
            pl.read_parquet(instruments_file) if instruments_file.exists() else None
        )

        return vxInstruments(instruments_name, inst_records)


class vxFeaturesProvider:
    def __init__(self, feature_path=".data") -> None:
        self._feature_path = Path(feature_path)

    def __call__(
        self,
        instruments: List[InstrumentType],
        start_date: DateTimeType = None,
        end_date: DateTimeType = None,
        freq: str = "1d",
        features: List[str] = None,
    ) -> pl.DataFrame:
        """获取行情通用接口

        Arguments:
            instruments {List[InstrumentType]} -- 需要下载的证券类型
            features: List[str] -- 行情列表
            freq: str -- 行情周期，只支持: {'1d'/'1min'}
            start_date {DateTimeType} -- 开始时间
            end_date {DateTimeType} -- 结束时间

        Returns:
            pl.DataFrame -- 返回： [trade_date, symbol, open, high, low, close, yclose, volume, amount, turnover_rate, volume_ratio,openinerest] 的列表
        """
        start_date = to_datetime(start_date or "2005-01-01")
        end_date = to_datetime(end_date or vxtime.today())
        freq = "day" if freq == "1d" else "min"
        features = features or [
            "trade_date",
            "symbol",
            "open",
            "high",
            "low",
            "close",
            "yclose",
            "pct_chg",
            "volume",
            "amount",
            "turnover_rate",
            "volume_ratio",
        ]

        data = pl.scan_parquet(
            Path(self._feature_path, "day_features.parquet"),
        )

        return (
            data.filter(
                (pl.col("symbol").is_in(instruments))
                & (pl.col("trade_date").is_between(start_date, end_date))
            )
            .sort(["trade_date", "symbol"])
            .collect()
            .select(features)
        )


class vxFactorsProvider:
    def __init__(self, db_file: Union[str, Path]) -> None:
        self._db_file = Path(db_file)
        try:
            self._db = pl.scan_parquet(db_file)
        except pl.ScanError:
            self._db = pl.DataFrame(
                {"trade_date": [], "symbol": []},
                schema={"trade_date": pl.Datetime, "symbol": str},
            )

    @property
    def database(self) -> pl.LazyFrame:
        return self._db

    def __call__(
        self,
        instruments: List[InstrumentType],
        start_date: DateTimeType = None,
        end_date: DateTimeType = None,
        freq: str = "1d",
        factors: List[str] = None,
    ) -> pl.DataFrame:
        start_date = to_datetime(start_date or "2005-01-01")
        end_date = to_datetime(end_date or vxtime.today())
        freq = "day" if freq == "1d" else "min"
        factors = factors or "*"

        return (
            self._db.filter(
                (pl.col("symbol").is_in(instruments))
                & (pl.col("trade_date").is_between(start_date, end_date))
            )
            .collect()
            .select(pl.col(factors))
        )

    def update_factors(self, factors: pl.DataFrame) -> None:
        """保存因子数据

        Arguments:
            factor {pl.DataFrame} -- factor： "trade_date", "symbol", "factor1","factor2"...
        """
        if isinstance(factors, pl.DataFrame):
            factors = factors.lazy()
        self._db = self._db.join(factors, on=["trade_date", "symbol"])


if __name__ == "__main__":
    from vxquant.model.nomalize import to_symbol

    with vxtime.timeit():
        f = vxFactorsProvider(
            "/Users/libao/src/开源代码/vxquant/.data/cn/day_stock_factors.parquet"
        )
        df = f.database.with_columns(
            [
                pl.col("ts_code").apply(to_symbol),
                pl.col("total_mv").log().alias("market_cap"),
                (1 / pl.col("pb")).alias("bm"),
            ]
        ).collect()

        print(df)
        df.select(pl.exclude("ts_code")).write_parquet(
            "/Users/libao/src/开源代码/vxquant/.data/cn/day_stock_factors.parquet"
        )
