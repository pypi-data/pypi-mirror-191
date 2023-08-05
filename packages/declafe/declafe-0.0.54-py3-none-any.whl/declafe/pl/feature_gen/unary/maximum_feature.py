import polars as pl

from declafe.pl.feature_gen.unary.unary_feature import UnaryFeature
from declafe.pl.feature_gen.types import ColLike


class MaximumFeature(UnaryFeature):

  def __init__(self, column: ColLike, comp: float):
    super().__init__(column)
    self.comp = comp

  def _unary_expr(self, orig_col: pl.Expr):
    return pl.when(orig_col > self.comp).then(orig_col).otherwise(self.comp)

  def _feature_names(self) -> list[str]:
    return [f"maximum({self.col_feature.feature_name}, {self.comp})"]
