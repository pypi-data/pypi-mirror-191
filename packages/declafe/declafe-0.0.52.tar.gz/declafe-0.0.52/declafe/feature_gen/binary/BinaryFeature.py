from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from ..FeatureGen import FeatureGen, ColLike


class BinaryFeature(FeatureGen, ABC):

  def __init__(self, left: ColLike, right: ColLike):
    super().__init__()
    self.left = self.to_col(left)
    self.right = self.to_col(right)
    self.left_f = self.to_col_feature_gen(left)
    self.right_f = self.to_col_feature_gen(right)

  @abstractmethod
  def bigen(self, left: np.ndarray, right: np.ndarray) -> np.ndarray:
    raise NotImplementedError()

  def _gen(self, df: pd.DataFrame) -> np.ndarray:
    return self.bigen(
        self.left_f.extract(df).to_numpy(),
        self.right_f.extract(df).to_numpy())
