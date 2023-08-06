from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from declafe.feature_gen import FeatureGen

if TYPE_CHECKING:
  from declafe import ColLike


class UnaryFeature(FeatureGen, ABC):

  def __init__(self, column_name: "ColLike"):
    super().__init__()
    self.orig_column_name = column_name
    self.column_name = self.to_col(column_name)

  @property
  @abstractmethod
  def name(self) -> str:
    """
    各featureクラスをインスタンス化したときにcolumn_nameを除外した名前
    e.g. PctChangeFeature(column="close", periods=5) => "pct_change_5"
    """
    raise NotImplementedError

  def _feature_name(self) -> str:
    from declafe.feature_gen.unary import IdFeature
    from declafe import ConstFeature
    name = self.column_name if isinstance(self.orig_column_name,
                                          (IdFeature, ConstFeature,
                                           str)) else f"({self.column_name})"
    return f"{self.name}_of_{name}"

  @property
  def column_f(self) -> FeatureGen:
    return self.to_col_feature_gen(self.column_name)

  def _gen(self, df: pd.DataFrame) -> np.ndarray:
    return self.gen_unary(self.column_f.extract(df).to_numpy())

  @abstractmethod
  def gen_unary(self, ser: np.ndarray) -> np.ndarray:
    raise NotImplementedError
