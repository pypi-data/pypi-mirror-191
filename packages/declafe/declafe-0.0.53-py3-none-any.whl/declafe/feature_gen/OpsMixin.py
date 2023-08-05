from abc import abstractmethod
from typing import TYPE_CHECKING, Any, cast, Union

if TYPE_CHECKING:
  from ..feature_gen import FeatureGen

O = Union["FeatureGen", int, float, str, bool]


class OpsMixin:

  @abstractmethod
  def _self(self) -> "FeatureGen":
    raise NotImplementedError

  @staticmethod
  def _bc():
    from declafe.feature_gen.binary import BiComposeFeature
    return BiComposeFeature

  @staticmethod
  def _conv(a: Any):
    from declafe.feature_gen.ConstFeature import ConstFeature
    return ConstFeature.conv(a)

  def __eq__(self, other: O) -> "FeatureGen":  # type: ignore
    from .binary import BiComposeFeature
    from .binary.ops import EqFeature

    return BiComposeFeature.make(left=self._self(),
                                 right=self._conv(other),
                                 to=EqFeature)

  def __ne__(self, other: O) -> "FeatureGen":  # type: ignore
    return (cast("FeatureGen", self) == other).flip_bool()

  def __add__(self, other: O) -> "FeatureGen":
    from declafe.feature_gen.binary import AddFeature
    return self._bc().make(left=self._self(),
                           right=self._conv(other),
                           to=AddFeature)

  def __radd__(self, other: O) -> "FeatureGen":
    return self.__add__(other)

  def __sub__(self, other: O) -> "FeatureGen":
    from declafe.feature_gen.binary import SubFeature

    return self._bc().make(self._self(), self._conv(other), SubFeature)

  def __rsub__(self, other: O) -> "FeatureGen":
    return self._conv(other).__sub__(self._self())

  def __mul__(self, other: O) -> "FeatureGen":
    from declafe.feature_gen.binary import MulFeature

    return self._bc().make(self._self(), self._conv(other), MulFeature)

  def __rmul__(self, other: O) -> "FeatureGen":
    return self.__mul__(other)

  def __mod__(self, other: O) -> "FeatureGen":
    from declafe.feature_gen.binary import ModFeature

    return self._bc().make(self._self(), self._conv(other), ModFeature)

  def __rmod__(self, other: O) -> "FeatureGen":
    return self._conv(other).__mod__(self._self())

  def __truediv__(self, other: O) -> "FeatureGen":
    from .binary.ops import DivideFeature

    return self._bc().make(self._self(), self._conv(other), DivideFeature)

  def __rtruediv__(self, other: O) -> "FeatureGen":
    return self._conv(other).__truediv__(self._self())

  def __gt__(self, other: O) -> "FeatureGen":
    from declafe.feature_gen.binary import GTFeature

    return self._bc().make(self._self(), self._conv(other), GTFeature)

  def __lt__(self, other: O) -> "FeatureGen":
    from declafe.feature_gen.binary import LTFeature

    return self._bc().make(self._self(), self._conv(other), LTFeature)

  def __ge__(self, other: O) -> "FeatureGen":
    from declafe.feature_gen.binary import GEFeature

    return self._bc().make(self._self(), self._conv(other), GEFeature)

  def __le__(self, other: O) -> "FeatureGen":
    from declafe.feature_gen.binary import LEFeature

    return self._bc().make(self._self(), self._conv(other), LEFeature)

  def __and__(self, other: O) -> "FeatureGen":
    from declafe.feature_gen.binary.ops.AndFeature import AndFeature

    return self._bc().make(self._self(), self._conv(other), AndFeature)

  def __rand__(self, other: O) -> "FeatureGen":
    return self.__and__(other)

  def __or__(self, other: O) -> "FeatureGen":
    from declafe.feature_gen.binary.ops.OrFeature import OrFeature

    return self._bc().make(self._self(), self._conv(other), OrFeature)

  def __ror__(self, other: O) -> "FeatureGen":
    return self.__or__(other)
