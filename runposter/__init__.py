__version__ = "0.0.1"

import logging
import sys
from dataclasses import dataclass

import drawsvg as draw
from rich.console import Console
from rich.progress import Progress

logger = logging.getLogger()

class Canvas:
  def __init__(self, shape, layout, source, width=841, height=1189):
    """
    The Canvas is the top-level drawing object.
    """
    self.shape  = shape
    self.layout = layout
    self.source = source
    self.width  = width
    self.height = height
    self.canvas = draw.Drawing(self.width, self.height, origin="center")
    logger.info(f"📋 canvas =  {self.width}x{self.height}")

  def render(self, df):
    """
    Render each activity in the dataset at the position determined by the layout.
    """
    with Progress(console=Console(file=sys.stderr)) as progress:
      task = progress.add_task("[red]rendering...", total=len(df))
      for activity, pos in zip(df.iterrows(), self.layout, strict=False):
        _, series = activity
        activity = self.source.create(series, df) # make statistics dict
        self.canvas.append(
          self.shape.render(activity).at(pos)
        )
        progress.update(task, advance=1)

    self.canvas.append(self.shape.legend)
    return self

  def __str__(self):
    """
    Provide the canvas as an SVG (XML) string.
    """
    return self.canvas.as_svg()

class Shape:
  def __init__(self):
    self.statistics = {}
    self.activity = {}
    self.left  = None
    self.top   = None
    self.angle = None
    self.legend = None

  def render(self, activity):
    self.activity = activity
    return self

  def at(self, pos):
    self.left  = pos[0]
    self.top   = pos[1]
    self.angle = pos[2]
    return self.rendered

  @property
  def circumradius(self):
    raise NotImplementedError

  @property
  def rendered(self):
    g = draw.Group(fill="none")
    for idx, (statistic, color) in enumerate(self.statistics.items()):
      visual = self.create_visual(statistic, index=idx, color=color)
      g.append(visual.at((self.left, self.top, 0)))
    return g

  def create_visual(self, statistic, index=0, color="red"):
    raise NotImplementedError

class Layout:
  def __init__(self, circumradius):
    self.circumradius = circumradius

  def __iter__(self):
    yield 0, 0, 0

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
    logger.debug(
      f"{self.name}: {self.min} .. {self.value} .. {self.max} = {p}"
    )
    return p

@dataclass
class Mapping:
  name : str
  max  : int | float | None = None
  min  : int | float | None = 0

class ActivityFactory:
  mapping : dict[str,Mapping] = {}

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
