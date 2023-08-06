"""文件系统存储数据库

/data/
.../cn/                     -----market
....../calendar.csv         -----日历文件
....../instruments/         -----股票池存储,[symbol, in_date, out_date, volume]
................../allstocks.csv
................../allcbonds.csv
................../allindexes.csv
................../alletflofs.csv
....../daybars/            -----存放行情相关内容 [trade_date, symbol, open, high, low, close, yclose, volume, amount, insterist, turnover]
............../2005.parquet
............../2006.parquet
............../2007.parquet
...
...../minbars/
............./200501.parquet
............./200502.parquet
............./200503.parquet
...
....../factors/             -----存放一些已经计算好的因子库 [ trade_date, symbol, [factor_name]]

"""

from pathlib import Path
from typing import Union


class FileStorage:
    def __init__(self, data_path: Union[str, Path], market: str = "cn") -> None:
        self._data_path = data_path
        self._market = "cn"
