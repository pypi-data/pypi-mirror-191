import polars as pl
import re
from typing import Union, List
from functions import DataFrameRolling
from .ops import FeatureOps, Feature


def to_expr(
    name: str, feature: str = None, over: Union[str, List[str]] = None
) -> pl.Expr:
    # Following patterns will be matched:
    # - $close -> Feature("close")
    # - $close5 -> Feature("close5")
    # - $open+$close -> Feature("open")+Feature("close")
    # TODO: this maybe used in the feature if we want to support the computation of different frequency data
    # - $close@5min -> Feature("close", "5min")

    if feature is None:
        feature = name

    # Chinese punctuation regex:
    # \u3001 -> 、
    # \uff1a -> ：
    # \uff08 -> (
    # \uff09 -> )
    chinese_punctuation_regex = r"\u3001\uff1a\uff08\uff09"
    for pattern, new in [
        (
            rf"\$\$([\w{chinese_punctuation_regex}]+)",
            r'PFeature("\1")',
        ),  # $$ must be before $
        (rf"\$([\w{chinese_punctuation_regex}]+)", r'Feature("\1")'),
        (r"(\w+\s*)\(", r"FeatureOps.\1("),
    ]:  # Features  # FeatureOps
        feature = re.sub(pattern, new, feature)

    return (
        eval(feature).over("symbol").alias(name) if over else eval(feature).alias(name)
    )
