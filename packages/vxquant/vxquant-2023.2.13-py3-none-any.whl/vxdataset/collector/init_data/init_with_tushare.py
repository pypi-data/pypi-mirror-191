"""下载数据目录"""

import argparse
import pandas as pd
import polars as pl
import tushare as ts
from pathlib import Path
from typing import List
from itertools import product
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from vxsched import vxContext
from vxquant.model.nomalize import to_symbol
from vxutils import logger, vxtime, to_datetime
from vxfactor.providers.calendar_cn import CNCalenderProvider
from vxfactor.instruments import vxInstruments


_default_config = {
    "ts_token": "854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c",
    "markets": ["cn"],
}


def download_all_stocklist(context, data_path):
    allstocks = vxInstruments("allstocks")

    df = pd.DataFrame()
    for status in ["L", "D", "P"]:
        data = ts.pro_api().stock_basic(
            exchange="", list_status=status, fields="ts_code, list_date, delist_date"
        )
        df = pd.concat([df, data])

    now = vxtime.today()

    for row in df.iterrows():
        try:
            allstocks.add_instrument(
                to_symbol(row[1]["ts_code"]),
                to_datetime(row[1]["list_date"]),
                to_datetime(row[1]["delist_date"] or now),
            )
        except Exception as e:
            logger.error(e)
    logger.info(f"加载以上是股票完成: {df.shape[0]}个")
    logger.info(f"allstocks: {allstocks}")
    allstocks.dump(Path(data_path, "cn", "instruments"))


def download_index_weight(context, data_path):
    """下载重要指数成分股及权重[000300.SH, 000905.SH, 000852.SH]"""
    indexs = {
        "CSI300": {
            "ts_code": "399300.SZ",
            "drange": [
                ("0101", "0331"),
                ("0401", "0630"),
                ("0701", "0930"),
                ("1001", "1231"),
            ],
        },
        "CSI500": {
            "ts_code": "000905.SH",
            "drange": [
                ("0101", "0331"),
                ("0401", "0630"),
                ("0701", "0930"),
                ("1001", "1231"),
            ],
        },
        "CSI1000": {
            "ts_code": "000852.SH",
            "drange": [
                ("0101", "0331"),
                ("0401", "0630"),
                ("0701", "0930"),
                ("1001", "1231"),
            ],
        },
        "BIGVALUE": {"ts_code": "399373.SZ", "drange": [("0101", "1231")]},
        "MADVALUE": {"ts_code": "399375.SZ", "drange": [("0101", "1231")]},
        "SMALLVALUE": {"ts_code": "399377.SZ", "drange": [("0101", "1231")]},
        "BIGGROW": {"ts_code": "399372.SZ", "drange": [("0101", "1231")]},
        "MADGROW": {"ts_code": "399374.SZ", "drange": [("0101", "1231")]},
        "SMALLGROW": {"ts_code": "399376.S", "drange": [("0101", "1231")]},
    }
    now = to_datetime(vxtime.now())

    for index, params in indexs.items():
        index_inst = vxInstruments(index)
        ts_code = params["ts_code"]

        idx_weights = pd.DataFrame()
        logger.info(f"{index}")
        for year, drange in tqdm(product(range(2010, now.year + 1), params["drange"])):
            start_date = f"{year}{drange[0]}"
            if to_datetime(start_date) > now:
                continue
            end_date = f"{year}{drange[1]}"

            df = ts.pro_api().index_weight(
                index_code=ts_code, start_date=start_date, end_date=end_date
            )
            if df.empty:
                logger.info(df)
                continue
            idx_weights = pd.concat([idx_weights, df])

        if idx_weights.empty:
            logger.warning(f"{index} 指数成分股信息为空.")
            vxtime.sleep(1)
            continue

        idx_weights["symbol"] = idx_weights["con_code"].apply(to_symbol)
        idx_weights = idx_weights.set_index(["trade_date", "symbol"])[
            "weight"
        ].sort_index()
        for trade_date, weights in idx_weights.unstack().iterrows():
            index_inst.update_components(
                weights.dropna().to_dict(), to_datetime(trade_date)
            )
        index_inst.dump(Path(data_path, "cn", "instruments"))
        logger.info(f"指数成分股{index} 更新完成: {index_inst} wait 1 seconds. ")
        vxtime.sleep(1)


def download_industry_sw_member(context, data_path):
    """下载申万一级行业成分股"""
    pro = ts.pro_api()
    df = pro.index_classify(level="L1", src="SW2021")

    for _, index in df[["index_code", "industry_name"]].iterrows():
        industry_inst = vxInstruments(f"sw2021_{index['industry_name']}行业")
        df = pro.index_member(index_code=index["index_code"])
        for _, in_out in tqdm(df[["con_code", "in_date", "out_date"]].iterrows()):
            industry_inst.add_instrument(
                in_out["con_code"],
                start_date=in_out["in_date"],
                end_date=in_out["out_date"] or vxtime.today(),
            )
        industry_inst.dump(Path(data_path, "cn", "instruments"))
        logger.info(f"行业下载完成 : {industry_inst}")


def init_calendar(context: vxContext, data_path: Path) -> None:
    """初始化calendar.csv"""
    logger.info("初始化全量交易日历....")
    trade_cal = CNCalenderProvider()
    cals = pl.DataFrame(trade_cal()).sort(by="trade_date")
    cals.write_parquet(Path(data_path, "calendar.parquet"))
    start_date = cals["trade_date"][0]
    end_date = cals["trade_date"][-1]
    logger.info(f"全量更新交易日历: {start_date} 至 {end_date}.")


def download_all_stock_daybars(context, data_path: Path) -> None:
    registrations = pl.read_parquet(
        Path(data_path, "cn", "instruments", "allstocks.parquet")
    )
    for symbol, start_date, end_date in tqdm(
        registrations.sort("start_date")
        .filter(pl.col("end_date") > to_datetime("2005-01-01"))
        .select(
            [
                "symbol",
                pl.col("start_date").apply(lambda x: max(x, to_datetime("2005-01-01"))),
                "end_date",
            ]
        )
        .rows()
    ):
        ts_code = f"{symbol[-6:]}.{symbol[:2]}"
        start_date = start_date.strftime("%Y%m%d")
        end_date = end_date.strftime("%Y%m%d")

        df = ts.pro_bar(
            ts_code=ts_code,
            start_date=start_date,
            end_date=end_date,
            asset="E",
            adj="qfq",
            factors=["tor", "vr"],
        )
        if df is None or df.empty:
            logger.warning(f"{symbol} can't get any data from tushare.")
            continue

        df = (
            pl.DataFrame(df)
            .with_columns(
                [
                    pl.col("trade_date").apply(to_datetime),
                    pl.col("ts_code").apply(to_symbol).alias("symbol"),
                    pl.col("pre_close").alias("yclose"),
                    pl.col("vol").alias("volume"),
                ]
            )
            .select(
                [
                    pl.col(
                        [
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
                    ),
                ]
            )
        )

        df.write_parquet(Path(data_path, "cn", "day", f"{symbol}.parquet"))


def download_stock_daily_basic_factors(context: vxContext, data_path: Path) -> None:
    from vxfactor.providers.calendar_cn import CNCalenderProvider

    trade_dates = CNCalenderProvider()("2005-01-01", vxtime.today())
    data = None
    pbar = tqdm(trade_dates)
    for trade_date in pbar:
        df = ts.pro_api().daily_basic(trade_date=trade_date.strftime("%Y%m%d"))
        if df is None or df.empty:
            logger.warning(f"{trade_date:%Y-%m-%d} 无法获取数据")
            continue
        pbar.set_description(f"处理交易日: {trade_date:%Y-%m-%d} 获取标的: {df.shape[0]}个")

        _data = pl.from_pandas(df)
        if data is None:
            data = _data
        else:
            data.extend(_data)
        vxtime.sleep(0.5)

    data.write_parquet(Path(data_path, "day_stock_factors.parquet"))


def init_stock_instruments(context: vxContext, data_path: Path) -> None:
    """初始化股票池

    包括: instrument_name, symbol,  listed_date, end_date, remark
    股票池分为3大类:
    1. "stock" --> 所有的股票，上市和退市都包括在内
    2、指数成分股 --> 某个指数对应的成分股
    3、行业成分股 --> 按照归属行业进行分类
    4、st股票池  --> ST/*ST股的股票池

    Arguments:
        context {vxContext} -- _description_
        data_path {Path} -- _description_
    """
    # download_all_stocklist(context, data_path)
    # download_index_weight(context, data_path)
    # download_industry_sw_member(context, data_path)
    # download_all_stock_daybars(context, data_path)
    download_stock_daily_basic_factors(context, data_path)


def main(configfile: str, data_path: str) -> None:
    configfile = Path(configfile)

    context = (
        vxContext.load_config(configfile, _default_config)
        if configfile.exists()
        else vxContext(_default_config)
    )
    context.executor = ProcessPoolExecutor()
    context.futures = []

    ts.set_token(context.ts_token)
    logger.info("初始化tushare 专业版接口.")
    data_path = Path(data_path)
    for market in context.markets:
        Path(data_path, market, "instruments").mkdir(parents=True, exist_ok=True)
        Path(data_path, market, "min").mkdir(parents=True, exist_ok=True)
        Path(data_path, market, "day").mkdir(parents=True, exist_ok=True)

    logger.info(f"初始化数据目录 {data_path} 完成.")

    # todo 下载calendar.csv
    with vxtime.timeit("init_calendar"):
        init_calendar(context, data_path)

    # todo 下载各类股票池:全部股票,停牌股票池，开盘涨停股票池,指数成分股、行业成分股
    with vxtime.timeit("init_stock_instruments"):
        init_stock_instruments(context, data_path)

    list(as_completed(context.futures))

    context.executor.shutdown(wait=True, cancel_futures=False)
    logger.info("执行完毕")
    del context.executor


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""初始化下载目录脚本""")

    parser.add_argument(
        "-c",
        "--config",
        help="path to config json file",
        default="config.json",
        type=str,
    )

    parser.add_argument(
        "-d",
        "--datapath",
        help="指定数据安装目录",
        default=".data/",
        type=str,
    )
    args = parser.parse_args()

    main(args.config, args.datapath)
