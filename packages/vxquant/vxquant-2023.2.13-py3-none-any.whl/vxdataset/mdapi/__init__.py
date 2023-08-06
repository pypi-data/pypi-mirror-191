import datetime
from typing import Any, Union

DateTimeType = Union[str, float, datetime.datetime, datetime.date, datetime.timedelta]
InstrumentType = str


class DataApiBase:
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__name__} api"
