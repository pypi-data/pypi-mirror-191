"""股票池"""

import polars as pl
from pathlib import Path
from typing import List, Union, Dict
from vxquant.model.nomalize import to_symbol
from vxutils import to_datetime, vxtime, to_timestamp, logger
from vxfactor.constants import DateTimeType, InstrumentType


def is_in_periods(dt, periods):
    dt = to_timestamp(dt) * 1_000_000
    return any(period[0] <= dt <= period[1] for period in periods)


class vxInstruments:
    def __init__(self, name: str, registrations: pl.DataFrame = None):
        self._name = name
        self._registrations = (
            registrations.with_columns(
                [
                    pl.col("start_date").apply(to_datetime),
                    pl.col("end_date").apply(to_datetime),
                ]
            )
            if registrations is not None
            else pl.DataFrame(
                {"symbol": [], "start_date": [], "end_date": [], "weight": []},
                schema={
                    "symbol": pl.Utf8,
                    "start_date": pl.Datetime,
                    "end_date": pl.Datetime,
                    "weight": pl.Float64,
                },
            )
        )
        self._last_updated_dt = (
            self._registrations["end_date"].max()
            if registrations is not None and (not registrations.is_empty())
            else to_datetime(vxtime.today())
        )

    def __str__(self) -> str:
        return (
            f"< 证券池({self._name}) 最近更新日期"
            f":{self._last_updated_dt:%Y-%m-%d}"
            f" 最新证券:\n {self.list_instruments(self._last_updated_dt)} >"
        )

    @property
    def registrations(self) -> pl.DataFrame:
        return self._registrations

    @property
    def last_updated_dt(self) -> DateTimeType:
        return self._last_updated_dt

    def list_instruments(self, trade_date: DateTimeType = None) -> List[InstrumentType]:
        trade_date = min(
            to_datetime(trade_date or vxtime.today()), self._last_updated_dt
        )

        inst = self._registrations.filter(
            ((pl.col("start_date") <= trade_date) & (pl.col("end_date") >= trade_date))
        )

        return inst["symbol"].to_list()

    def get_weights(self, trade_date: DateTimeType = None) -> List[float]:
        trade_date = min(
            to_datetime(trade_date or vxtime.today()), self._last_updated_dt
        )

        inst = self._registrations.filter(
            ((pl.col("start_date") <= trade_date) & (pl.col("end_date") >= trade_date))
        )
        return dict(*inst.select(["symbol", "weight"]).to_struct().arr)

    def to_stack_df(self, trade_dates: Union[List, pl.Series]) -> None:
        """转化为交易日期过滤格式

        trade_date, symbol, is_in
        """
        if isinstance(trade_dates, pl.Series):
            trade_dates = trade_dates.to_list()

        symbols = pl.DataFrame(
            {symbol: [] for symbol in self._registrations["symbol"].unique()}
        )
        stack_df = pl.concat(
            [
                pl.DataFrame({"trade_date": trade_dates}),
                symbols,
            ],
            how="horizontal",
        ).with_columns([pl.exclude("trade_date").cast(pl.Boolean).fill_null(False)])

        exprs = [
            pl.col("trade_date")
            .apply(lambda x: is_in_periods(x, row["period"]))
            .alias(row["symbol"])
            for row in (
                self._registrations.with_columns(
                    [pl.concat_list(["start_date", "end_date"]).alias("period")]
                )
                .groupby("symbol")
                .agg(pl.col(["period"]))
                .iter_rows(named=True)
            )
        ]
        return stack_df.with_columns(exprs).sort(by="trade_date")

    def add_instrument(
        self,
        symbol: InstrumentType,
        start_date: DateTimeType,
        end_date: DateTimeType = None,
        weight: float = 1.0,
    ):
        try:
            symbol = to_symbol(symbol)
            start_date = to_datetime(start_date)
            end_date = to_datetime(end_date) if end_date else start_date
        except Exception as e:
            logger.error(f"ValueError: {e}")
            return

        self._registrations.vstack(
            pl.DataFrame(
                [
                    {
                        "symbol": symbol,
                        "start_date": start_date,
                        "end_date": end_date,
                        "weight": weight,
                    }
                ]
            ),
            in_place=True,
        )

    def update_components(
        self, instruments: Dict[InstrumentType, float], updated_dt: DateTimeType = None
    ):
        """按增量更新股票池"""

        updated_dt = to_datetime(updated_dt or vxtime.today())
        if (not self._registrations.is_empty()) and self._last_updated_dt >= updated_dt:
            raise ValueError(
                f"updated_dt( {updated_dt:%Y-%m-%d} ) 小于当前更新时间:"
                f" {self._last_updated_dt:%Y-%m-%d}"
            )
        if isinstance(instruments, list):
            instruments = {inst: 1 for inst in instruments}

        new_instruments = pl.DataFrame(
            [
                {"symbol": symbol, "end_date": self._last_updated_dt, "weight": weight}
                for symbol, weight in instruments.items()
            ]
        )

        self._registrations = (
            self._registrations.join(
                new_instruments, on=["symbol", "end_date"], how="outer"
            )
            .with_columns(
                [
                    pl.col("start_date").fill_null(updated_dt),
                    pl.when(
                        (pl.col("end_date") == self._last_updated_dt)
                        & (pl.col("symbol").is_in(new_instruments["symbol"]))
                    )
                    .then(pl.lit(updated_dt))
                    .otherwise(pl.col("end_date"))
                    .alias("end_date"),
                    pl.when(
                        (pl.col("end_date") == self._last_updated_dt)
                        & (pl.col("symbol").is_in(new_instruments["symbol"]))
                    )
                    .then(pl.col("weight_right"))
                    .otherwise(pl.col("weight"))
                    .alias("weight"),
                ]
            )
            .select(["symbol", "start_date", "end_date", "weight"])
            .sort(by="end_date")
        )
        self._last_updated_dt = updated_dt

    @classmethod
    def load(cls, name, instruments_parquet: Union[str, Path]) -> "vxInstruments":
        registrations = pl.read_parquet(instruments_parquet)
        return vxInstruments(name, registrations)

    def dump(self, instruments_parquet: Union[str, Path]) -> None:
        """保存相关信息"""
        if Path(instruments_parquet).is_dir():
            instruments_parquet = Path(instruments_parquet, f"{self._name}.parquet")

        self._registrations.write_parquet(instruments_parquet)
        logger.info(f"股票池:{self._name} 保存{instruments_parquet.as_posix()} 完成。")
        return self
