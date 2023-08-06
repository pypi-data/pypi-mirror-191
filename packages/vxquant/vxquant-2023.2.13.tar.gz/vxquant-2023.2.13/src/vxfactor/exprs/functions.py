import polars as pl
import numpy as np
from collections import deque
from typing import Callable
from vxutils import logger


# @pl.api.register_dataframe_namespace("rolling_apply")
@pl.api.register_expr_namespace("rolling")
class DataFrameRolling:
    def __init__(self, expr):
        self._expr = expr
        self._func = None
        self._windows = None
        self._queues = None

    def __call__(self, cols, func, windows_size):
        if self._func is None:
            self._func = func
            self._windows = windows_size
            self._queues = [
                deque([np.nan] * self._windows, maxlen=self._windows)
                for _ in range(len(cols) + 1)
            ]

        # return self._df.with_columns([pl.concat_list(cols).apply(self.warpped_func)])
        _cols = [self._expr]
        _cols.extend(cols)
        return [pl.concat_list(_cols).rolling_apply(self.warpped_func)]

    def warpped_func(self, args: pl.Series) -> pl.Series:
        for arg, queue in zip(args, self._queues):
            queue.append(arg)
        new_args = [(pl.Series(queue)) for queue in self._queues]
        return self._func(*new_args)


class vxRollingApply:
    def __init__(self, *exprs) -> None:
        self._exprs = exprs
        self._queue = None
    
    def __call__(self, func:Callable, windows_size:int) -> pl.Series:
        


class ColsRolling:
    def __init__(self, func: Callable, windows: int):
        self._func = func
        self._windows = windows
        self._args = None
        self._cnt = 0

    def __call__(self, s: pl.Series):
        if self._args is None:
            self._args = [
                deque([np.nan] * self._windows, maxlen=self._windows)
                for _ in range(len(s))
            ]
            self._cnt = 0

        new_args = []
        for new_arg, args_queue in zip(s, self._args):
            args_queue.append(new_arg)
            new_args.append(pl.lit(pl.Series(args_queue)))

        self._cnt += 1
        if self._cnt < self._windows:
            return np.nan

        try:
            return self._func(*new_args)
        except Exception as e:
            logger.error(e)
            return np.nan


def rolling_apply_cols(exprs, func, windows):
    return pl.concat_list(exprs).apply(ColsRolling(func, windows))


if __name__ == "__main__":
    df = pl.DataFrame(
        {
            "a": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
            ],
            "b": [5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16],
        },
        # schema={"a": pl.Int32, "b": pl.Int32},
    )
    # print(df)

    def test(x, y):
        print("=" * 60)
        print(x, y)
        return np.corrcoef(x, y)[0, 1]

    def corr(x, y):
        return x.pearson_corr(y)

    print(df.with_columns([pl.col("a").rolling(["a", "b"], pl.pearson_corr, 5)]))
