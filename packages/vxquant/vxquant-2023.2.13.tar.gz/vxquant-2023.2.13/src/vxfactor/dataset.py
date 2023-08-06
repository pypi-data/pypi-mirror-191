import polars as pl
import datetime
from pathlib import Path
from typing import Union, List
from tqdm import tqdm
from vxutils import to_datetime, vxtime
from vxfactor.mdapi import mdapi
from vxfactor.exprs.ops import ops_register
from vxfactor.exprs import to_expr
from vxfactor.instruments import vxInstruments
from vxfactor.providers import InstrumentType, DateTimeType


def _normalize(series: pl.Series, n=3) -> pl.Series:
    """去极值化"""
    median = series.median()
    new_median = ((series - median).abs()).median()
    series = series.clip(median - n * new_median, median + n * new_median)
    return (series - series.mean()) / series.std()


class vxDataset:
    def __init__(self, name: str, data_path: Union[str, Path] = ".data") -> None:
        self._name = name
        self._data_path = data_path
        self._data = pl.DataFrame(
            {"trade_date": [], "symbol": [], "available": []},
            schema={"trade_date": pl.Datetime, "symbol": str, "available": pl.Boolean},
        )

        self._all_instruments = None
        self._start_date = None
        self._end_date = None
        self._trade_dates = []
        self._factors = []

    @property
    def data(self) -> pl.DataFrame:
        if isinstance(self._data, pl.LazyFrame):
            with vxtime.timeit("导出数据...", show_title=True):
                self._data = self._data.collect(streaming=True)
        return self._data

    def set_instruments(
        self,
        instruments: Union[str, vxInstruments, List[InstrumentType]],
        start_date: DateTimeType = "2005-01-01",
        end_date: DateTimeType = None,
    ) -> "vxDataset":
        """设置数据股票池

        Keyword Arguments:
            instruments: {Union[vxInstruments, List[InstrumentType]]} -- 设置股票池
            start_date {DateTimeType} -- 数据集开始时间 (default: {'2005-01-01'})
            end_date {DateTimeType} -- 数据集结束时间  (default: {None})

        处理数据结果data:  [trade_date, symbol, available]
        """
        start_date = to_datetime(start_date)
        end_date = to_datetime(end_date or vxtime.today())
        if isinstance(instruments, list):
            inst = vxInstruments(self._name)
            for symbol in instruments:
                inst.add_instrument(symbol, start_date, end_date)

        elif isinstance(instruments, str):
            inst = mdapi.instruments(instruments)
        else:
            inst = instruments

        self._trade_dates = mdapi.calendar(start_date, end_date)
        self._start_date = self._trade_dates.min()
        self._end_date = self._trade_dates.max()
        self._all_instruments = inst.registrations["symbol"].unique()

        with vxtime.timeit("制作交易标的日历清单"):
            pbar = tqdm(self._trade_dates, desc="制作交易标的日历清单")
            for trade_date in pbar:
                pbar.set_description(f"制作交易标的日历 {trade_date:%Y-%m-%d}")
                symbols = inst.list_instruments(trade_date)
                if len(symbols) == 0:
                    continue

                self._data.extend(
                    pl.DataFrame(
                        {
                            "symbol": self._all_instruments,
                        }
                    ).select(
                        [
                            pl.lit(to_datetime(trade_date)).alias("trade_date"),
                            pl.col("symbol"),
                            pl.col("symbol").is_in(symbols).alias("available"),
                        ]
                    )
                )

        return self

    def skip_new_stock(self, n: int = 180) -> "vxDataset":
        """过滤上市n个自然日的股票

        Returns:
            vxDataset -- _description_
        """
        with vxtime.timeit(f"剔除上市未超过{n}天证券"):
            allstocks_list = mdapi.instruments("allstocks").registrations
            allstocks_list = (
                allstocks_list.with_columns(
                    [
                        (pl.col("start_date") + datetime.timedelta(days=n)).alias(
                            "normal_date"
                        )
                    ]
                )
                .filter(pl.col("normal_date") <= pl.col("end_date"))
                .sort("normal_date")
            )

            self._data = (
                self._data.lazy()
                .join(allstocks_list.lazy(), on="symbol", how="left")
                .with_columns(
                    [
                        pl.when((pl.col("trade_date") < pl.col("normal_date")))
                        .then(pl.lit(False))
                        .otherwise(pl.col("available"))
                        .alias("available")
                    ]
                )
                .select(["trade_date", "symbol", "available"])
            )
        return self

    def load_features(self, fields: List[str] = None) -> "vxDataset":
        """加载已保存指标以及因子

        Arguments:
            fields {List[str]} -- 需要加载的因子名称列表

        Returns:
            vxDataset -- _description_
        """
        with vxtime.timeit("加载指标以及因子", show_title=True):
            df = mdapi.features(
                self._all_instruments,
                self._start_date,
                self._end_date,
            )
            self._data = (
                self._data.lazy()
                .join(df.lazy(), on=["trade_date", "symbol"], how="outer")
                .drop_nulls()
                .sort("trade_date")
            )
        return self

    def build_factors(self, **factors) -> "vxDataset":
        """计算因子值

        如： build_factors(ma5='MEAN($close, 5)', ma10='MEAN($close, 10)')

        Returns:
            vxDataset -- _description_
        """
        with vxtime.timeit("计算因子值"):
            exprs = [
                to_expr(name, factor_expr, "symbol")
                for name, factor_expr in factors.items()
            ]
            self._data = self._data.with_columns(exprs)
        self._factors.extend(factors.keys())
        return self

    def nomalize_factors(self, *factors: List[str]) -> "vxDataset":
        """标准化相关因子
        1、去极值
        2、标准化
        #3、市值以及行业中性化

        Returns:
            vxDataset -- _description_
        """
        if len(factors) == 1 and isinstance(factors[0], list):
            factors = factors[0]

        with vxtime.timeit(f"去极值、标准化{factors or self._factors}"):
            factors = pl.col(factors) if factors else pl.col(self._factors)

            self._data = (
                self._data.drop_nulls()
                .filter(pl.col("available"))
                .with_columns([factors.apply(_normalize).over("trade_date")])
            )

        return self

    def neutralization(self, *factors: List[str]) -> "vxDataset":
        """行业及市值中性化

        Returns:
            vxDataset -- _description_
        """


if __name__ == "__main__":
    print(pl.threadpool_size())
    vxtime.sleep(10)
    dataset = vxDataset("alpha158")
    with vxtime.timeit():
        data = dataset.set_instruments("CSI500").skip_new_stock(180).data
        dataset.load_features()
        dataset.build_factors(
            vmom5="EMA($close/$amount*10000, 5)",
            vmom10="EMA($close/$amount*10000, 10)",
            vmom20="EMA($close/$amount*10000, 20)",
            vmom30="EMA($close/$amount*10000, 30)",
            # ma5="MA($close,$high,5)",
            #            corr5="Corr($close, $high,20)",
        )
        # print(dataset.data.tail(5))
        dataset.nomalize_factors()
        print(dataset.data.tail(5))

        # print(
        #    dataset.data.with_columns(
        #        pl.concat_list(["close", "amount"]).rolling_apply(func, 10)
        #    )
        #
        # )

    # print(mdapi.features(["SZSE.300604"]))

    # print(dataset._data)
