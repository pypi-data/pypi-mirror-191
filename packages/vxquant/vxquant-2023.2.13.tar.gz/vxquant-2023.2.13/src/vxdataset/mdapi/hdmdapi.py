"""行情接口"""
import polars as pl
from pathlib import Path
from typing import List
from vxutils import vxtime, logger, vxWrapper, to_datetime
from vxdataset.mdapi import DateTimeType
from vxdataset.mdapi.instruments import vxInstruments


class vxMdApi:
    def __init__(self, data_path: str = ".data/", market: str = "cn") -> None:
        self._data_path = Path(data_path, market)
        if not self._data_path.exists():
            raise ValueError("目录没有初始化，请先初始化数据目录")

        self._market = market
        self._tickcache = {}
        self._last_cache_dt = 0
        self.register(
            get_trade_dates={
                "class": "vxdataset.collector.calendar.base.CNCalender",
                "params": {},
            },
            hq={"class": "vxdataset.collector.hq.tdx.vxHqAPI", "params": {}},
        )

    def register(self, **apis):
        """注册一个api接口"""
        for name, api in apis.items():
            api = vxWrapper.init_by_config(api)
            if not callable(api):
                logger.warning(f"{name} 的API接口无法调用 {api}.")
                continue
            self.__dict__[name] = api
            logger.info(f"注册{name}接口成功 {api}")

    def calendar(
        self, start_date: DateTimeType, end_date: DateTimeType = None
    ) -> List[DateTimeType]:
        start_date = to_datetime(start_date)
        end_date = to_datetime(end_date or vxtime.now())
        cal_parquet = Path(self._data_path, "calendar.parquet")
        if not cal_parquet.exists():
            trade_dates = pl.DataFrame(
                {"trade_date": self.get_trade_dates(market=self._market)}
            )
            trade_dates.write_parquet(cal_parquet.as_posix())

        return pl.read_parquet(cal_parquet.as_posix())["trade_date"].filter(
            ((pl.col("trade_date") >= start_date) & (pl.col("trade_date") <= end_date))
        )

    def current(self, *symbols) -> List:
        """实时行情接口"""
        if len(symbols) == 1 and isinstance(symbols[0], str):
            symbols = symbols[0]

        if self._last_cache_dt + 3 > vxtime.now():
            _missing_symbols = set(symbols).union(set(self._tickcache.keys()))
            self._last_cache_dt = vxtime.now()
        else:
            _missing_symbols = set(symbols).difference(set(self._tickcache.keys()))

        if _missing_symbols:
            ticks = self.hq(*_missing_symbols)
            self._tickcache.update(ticks)

        return {
            symbol: self._tickcache[symbol]
            for symbol in symbols
            if symbol in self._tickcache
        }

    def instruments(
        self,
        instrument_name: str = "allstocks",
    ) -> vxInstruments:
        """股票池

        Arguments:
            instrument_name {str} --

        Returns:
            vxInstruments -- 股票池类别
        """
        inst_data_path = Path(
            self._data_path, "instruments", f"{instrument_name}.parquet"
        )
        return vxInstruments.load(instrument_name, inst_data_path)


if __name__ == "__main__":
    mdapi = vxMdApi()
    # with vxtime.timeit():
    #    df = pl.DataFrame(
    #        tick.message
    #        for tick in mdapi.current(
    #            "SHSE.600000",
    #            "SZSE.000001",
    #            "SHSE.000001",
    #            "SHSE.000688",
    #            "SHSE.511880",
    #            "SHSE.510300",
    #            "SHSE.511990",
    #            "SHSE.511660",
    #            "SHSE.204001",
    #            "SZSE.399001",
    #            "SZSE.399673",
    #            "SZSE.159001",
    #            "SZSE.159919",
    #            "SZSE.159915",
    #            "SZSE.159937",
    #            "SZSE.131810",
    #        ).values()
    #    )
    # print(df)

    inst = mdapi.instruments("CSI500")
    symbols = inst.list_instruments()["symbol"].to_list()
    print(len(symbols))

    with vxtime.timeit():
        ticks = mdapi.current(*symbols)
    df = pl.DataFrame(
        [tick.message for tick in ticks.values()],
    )
    print(
        df.select(
            [
                pl.col("symbol"),
                pl.col("lasttrade"),
                (pl.col("lasttrade") / pl.col("yclose") * 100 - 100.0).alias(
                    "pct_change"
                ),
            ]
        ).sort(by="pct_change", reverse=True)
    )
