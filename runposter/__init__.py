__version__ = "0.0.1"

from dataclasses import dataclass, field
from typing import Union, Dict

from datetime import datetime

import drawsvg as draw

import logging
logger = logging.getLogger()

class Canvas:
  def __init__(self, shape, layout, source, width=841, height=1189):
    self.shape  = shape
    self.layout = layout
    self.source = source
    self.width  = width
    self.height = height
    self.canvas = draw.Drawing(self.width, self.height, origin="center")

  def render(self, df):

    for activity, pos in zip(df.iterrows(), self.layout):
      _, series = activity
      activity = self.source.create(series, df)
      self.canvas.append(
        self.shape.render(activity).at(pos)
      )
    return self

  def __str__(self):
    return self.canvas.as_svg()

class Shape:
  def __init__(self):
    self.activity = None

  def render(self, activity):
    self.activity = activity
    return self

  def at(self, pos):
    self.left = pos[0]
    self.top  = pos[1]
    return self.rendered

  @property
  def circumradius(self):
    raise NotImplementedError

  @property
  def rendered(self):
    raise NotImplementedError

class Layout:
  def __init__(self, circumradius):
    self.circumradius = circumradius

class Statistic:
  def __init__(self, name, value, df, mapping):
    self.name    = name
    self.value   = value
    self.df      = df
    self.mapping = mapping

  @property
  def min(self):
    if self.mapping.min is not None:
      return self.mapping.min
    return self.df[self.name].min()

  @property
  def max(self):
    if self.mapping.max is not None:
      return self.mapping.max
    return self.df[self.name].max()

  @property
  def pct(self):
    p = (self.value - self.min) / (self.max - self.min)
    logger.debug(f"{self.name}: {self.min} .. {self.value} .. {self.max} = {p}")
    return p

@dataclass
class Mapping:
  name : str
  max  : Union[int,float,None] = None
  min  : Union[int,float,None] = 0

class ActivityFactory:
  mapping : Dict[str,Mapping] = {}

  @classmethod
  def create(cls, series, df):
    return {
      mapping.name : Statistic(name, series.get(name), df, mapping)
      for name, mapping in cls.mapping.items()
    }

  @classmethod
  def props(cls):
    return {
      mapping.name : name for name, mapping in cls.mapping.items()
    }
