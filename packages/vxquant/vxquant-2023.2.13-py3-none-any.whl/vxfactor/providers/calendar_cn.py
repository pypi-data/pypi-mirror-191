"""交易日期基础接口"""

import time
import requests
import random
import datetime
import polars as pl
from itertools import product

from vxfactor.providers import vxCalendarProvider
from vxutils import vxtime, to_datetime, logger
from typing import List
from tqdm import tqdm

SSE_CALENDAR_LIST = "http://www.szse.cn/api/report/exchange/onepersistenthour/monthList?month={year}-{month}&random={timestamp}"


class CNCalenderProvider(vxCalendarProvider):
    def get_trade_dates(self, market: str = "cn") -> List:
        if market != "cn":
            raise NotImplementedError(f"暂不支持 {market}类型")

        start_date = datetime.datetime(2005, 1, 1)
        end_date = datetime.datetime.now().replace(
            month=12, day=31, hour=0, minute=0, second=0
        )

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
                            trade_date["jyrq"]
                            for trade_date in reply["data"]
                            if trade_date["jybz"] == "1"
                        ]
                    )
                except Exception as e:
                    logger.error(f"{year}-{month} get calendar {reply} error: {e}")
                vxtime.sleep(0.1)
        return sorted(cals)


if __name__ == "__main__":
    from vxutils import diskcache, vxtime

    c = CNCalenderProvider()
    with vxtime.timeit():
        a = c("2022-01-01")
    print(a[:10])
    print(diskcache)
