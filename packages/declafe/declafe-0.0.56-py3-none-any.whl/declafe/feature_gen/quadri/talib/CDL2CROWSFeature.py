import numpy as np
import talib

from declafe import ColLike
from declafe.feature_gen.quadri.QuadriFeature import QuadriFeature

__all__ = ["CDL2CROWSFeature"]


class CDL2CROWSFeature(QuadriFeature):

  def __init__(self, opn: ColLike, high: ColLike, low: ColLike, close: ColLike):
    super().__init__(opn, high, low, close)

  def quadrigen(self, col1: np.ndarray, col2: np.ndarray, col3: np.ndarray,
                col4: np.ndarray) -> np.ndarray:
    return talib.CDL2CROWS(col1.astype(float), col2.astype(float),
                           col3.astype(float), col4.astype(float))

  def _feature_name(self) -> str:
    return f"CDL2CROWS_{self.col1}_{self.col2}_{self.col3}_{self.col4}"
