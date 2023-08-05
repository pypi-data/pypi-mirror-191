import functools
from dataclasses import dataclass, field
from typing import List, Type, Callable, Union, TYPE_CHECKING, TypeVar, Iterable, cast

__all__ = ["Features", "F"]

import pandas as pd
from tqdm import tqdm

from declafe.feature_gen.types import DTypes

if TYPE_CHECKING:
  from declafe.feature_gen.FeatureGen import FeatureGen

from declafe.feature_gen.unary import UnaryFeature

T = TypeVar("T")
Ap = Callable[[T], "Features"]
Fun = Callable[[T], "FeatureGen"]


@dataclass
class Features:
  feature_gens: List["FeatureGen"]
  pre_processes: List["FeatureGen"] = field(default_factory=list)

  def __post_init__(self):
    """
    Remove duplicated features and pre_processes
    """
    fs: List["FeatureGen"] = []

    for fe in self.feature_gens:
      if all([not f.equals(fe) for f in fs]):
        fs.append(fe)

    ps: List["FeatureGen"] = []

    for pre in self.pre_processes:
      if all([not p.equals(pre) for p in ps]):
        ps.append(pre)

    self.feature_gens = fs
    self.pre_processes = ps

  def __call__(self,
               temp_df: pd.DataFrame,
               show_progress: bool = False,
               drop_nan: bool = False):
    return self.set_features(temp_df, show_progress, drop_nan)

  def set_features(self,
                   temp_df: pd.DataFrame,
                   show_progress: bool = False,
                   drop_nan: bool = False) -> pd.DataFrame:
    df = temp_df
    for p in self.pre_processes:
      df = p.set_feature(df)

    if show_progress:
      with tqdm(total=self.feature_count) as t:
        for feature_gen in self.feature_gens:
          t.set_description(f"Gen: {feature_gen.feature_name}")
          df = feature_gen.set_feature(df)
          t.update()
    else:
      for feature_gen in self.feature_gens:
        df = feature_gen.set_feature(df)

    if drop_nan:
      df.dropna(inplace=True)

    return df

  @property
  def feature_names(self) -> List[str]:
    return [f.feature_name for f in self.feature_gens]

  def unary_feature_name_of(self, column_name: str) -> List[str]:
    return [
        f.feature_name
        for f in self.feature_gens
        if isinstance(f, UnaryFeature) and f.column_name == column_name
    ]

  def contains(self, feature: "FeatureGen") -> bool:
    return feature.feature_name in self.feature_names

  def __contains__(self, item: "FeatureGen") -> bool:
    return self.contains(item)

  def __add__(self, other):
    return Features(self.feature_gens + [
        f for f in other.feature_gens
        if f.feature_name not in self.feature_names
    ])

  def add_feature(self, feature_gen: "FeatureGen"):
    return Features(self.feature_gens + [feature_gen], self.pre_processes)

  def add_features(self, feature_gens: List["FeatureGen"]):
    return Features(self.feature_gens + feature_gens, self.pre_processes)

  def show_features(self) -> None:
    for f in self.feature_gens:
      print(f.feature_name)

  def filter_by_name(self, feature_names: List[str]):
    return Features(
        [f for f in self.feature_gens if f.feature_name in feature_names])

  def filter_not_by_name(self, feature_names: List[str]):
    return Features(
        [f for f in self.feature_gens if f.feature_name not in feature_names])

  def filter_by_dtype(self, dtypes: Union[DTypes, List[DTypes]]) -> "Features":
    if isinstance(dtypes, str):
      dtypes = [dtypes]

    return Features([f for f in self if f.dtype in dtypes])

  def filter_not_by_dtype(self, dtypes: Union[DTypes,
                                              List[DTypes]]) -> "Features":
    if isinstance(dtypes, str):
      dtypes = [dtypes]

    return Features([f for f in self if f.dtype not in dtypes])

  def filter(self, feature: List["FeatureGen"]):
    return Features(
        [f for f in self.feature_gens if Features(feature).contains(f)])

  def filter_not(self, features: List["FeatureGen"]) -> "Features":
    return Features(
        [f for f in self.feature_gens if not Features(features).contains(f)])

  def filter_gen(self, cls: Type["FeatureGen"]):
    return Features([f for f in self.feature_gens if isinstance(f, cls)])

  def filter_not_gen(self, cls: Type["FeatureGen"]):
    return Features([f for f in self.feature_gens if not isinstance(f, cls)])

  def reduce(self, f: Callable[["FeatureGen", "FeatureGen"], "FeatureGen"],
             initial: "FeatureGen"):
    return functools.reduce(f, self.feature_gens, initial)

  _F = Union[Type["UnaryFeature"], Callable[["FeatureGen"], "FeatureGen"]]

  def map(self, f: _F, **kwargs) -> "Features":
    if isinstance(f, UnaryFeature.__class__):  # type: ignore
      return Features([
          fg.next(cast(Type[UnaryFeature], f), **kwargs)
          for fg in self.feature_gens
      ])
    else:
      return Features([f(fg) for fg in self.feature_gens])  # type: ignore

  _FM = Callable[["FeatureGen"], Union["Features", List["FeatureGen"]]]

  def flat_map(self, fun: _FM) -> "Features":
    return Features([f for fg in self.feature_gens for f in fun(fg)])

  def zip_with(self, fs: "Features", f: Callable[["FeatureGen", "FeatureGen"],
                                                 "FeatureGen"]):
    return Features(
        [f(f1, f2) for f1, f2 in zip(self.feature_gens, fs.feature_gens)])

  def extract(self, df: pd.DataFrame) -> pd.DataFrame:
    return df[self.feature_names]

  def as_type_auto_num_all(self, override: bool = False):
    return self.map(lambda f: f.as_type_auto_num(override))

  def enable_numba(self) -> "Features":
    return self.map(lambda f: f.enable_numba())

  def disable_numba(self) -> "Features":
    return self.map(lambda f: f.disable_numba())

  @property
  def feature_count(self) -> int:
    return len(self.feature_gens)

  def __len__(self) -> int:
    return self.feature_count

  @staticmethod
  def empty() -> "Features":
    return Features([])

  @staticmethod
  def one(feature_gen: "FeatureGen") -> "Features":
    return Features([feature_gen])

  @staticmethod
  def two(feature_gen1: "FeatureGen", feature_gen2: "FeatureGen") -> "Features":
    return Features([feature_gen1, feature_gen2])

  @staticmethod
  def many(*args: "FeatureGen") -> "Features":
    return Features(list(args))

  @staticmethod
  def iter_over(it: Iterable[T]) -> Ap:

    def ap(f: Fun) -> "Features":
      return Features([f(x) for x in it])

    return ap

  def __iter__(self):
    return self.feature_gens.__iter__()


F = Features
