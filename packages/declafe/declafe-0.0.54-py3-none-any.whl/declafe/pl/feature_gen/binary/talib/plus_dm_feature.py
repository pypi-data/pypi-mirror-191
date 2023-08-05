import polars as pl
from declafe.pl.feature_gen.types import ColLike
import talib
from typing import cast

from declafe.pl.feature_gen.binary.binary_feature import BinaryFeature


class PLUS_DMFeature(BinaryFeature):

  def __init__(self, high: ColLike, low: ColLike, timeperiod: int = 14):
    super().__init__(high, low)
    self.timeperiod = timeperiod

  def _binary_expr(self, left: pl.Expr, right: pl.Expr) -> pl.Expr:
    return cast(pl.Expr, pl.struct([left, right])).map(lambda s: talib.PLUS_DM(
        s.apply(lambda ss: ss[f'{self.left_feature.feature_name}']),
        s.apply(lambda ss: ss[f'{self.right_feature.feature_name}']),
        timeperiod=self.timeperiod))

  def _feature_names(self) -> list[str]:
    return [
        f'PLUS_DM({self.timeperiod})({self.left_feature.feature_name}, {self.right_feature.feature_name})'
    ]
