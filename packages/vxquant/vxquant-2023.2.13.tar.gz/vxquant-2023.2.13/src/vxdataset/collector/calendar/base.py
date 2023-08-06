"""交易日期基础接口"""

import time
import requests
import random
import datetime
import polars as pl
from itertools import product

from vxdataset.mdapi import DataApiBase
from vxutils import vxtime, to_datetime, logger
from typing import List
from tqdm import tqdm

SSE_CALENDAR_LIST = "http://www.szse.cn/api/report/exchange/onepersistenthour/monthList?month={year}-{month}&random={timestamp}"


class CNCalender(DataApiBase):
    def __call__(
        self,
        start_date: datetime.datetime = None,
        end_date: datetime.datetime = None,
        market: str = "cn",
    ) -> List:
        if market != "cn":
            raise NotImplementedError(f"暂不支持 {market}类型")

        if start_date is None:
            start_date = datetime.datetime(2005, 1, 1)

        now = datetime.datetime.now()
        if end_date is None:
            end_date = now.replace(month=12, day=31, hour=0, minute=0, second=0)

        cals = []
        for year, month in tqdm(
            product(range(start_date.year, end_date.year + 1), range(1, 13))
        ):
            url = SSE_CALENDAR_LIST.format(
                year=year, month=month, timestamp=random.randint(100000, 10000000)
            )
            resp = requests.get(url, timeout=1)
            resp.raise_for_status()
            reply = resp.json()
            if "data" in reply and reply["data"]:
                try:
                    cals.extend(
                        [
                            {
                                "trade_date": trade_date["jyrq"],
                                "cn": bool(trade_date["jybz"]),
                            }
                            for trade_date in reply["data"]
                        ]
                    )
                except Exception as e:
                    logger.error(f"{year}-{month} get calendar {reply} error: {e}")
                vxtime.sleep(0.1)
        return cals
