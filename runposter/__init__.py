__version__ = "0.0.1"

from dataclasses import dataclass, field
from typing import Union

from datetime import datetime

import drawsvg as draw

class Canvas:
  def __init__(self, shape, layout, width=841, height=1189):
    self.shape      = shape
    self.layout     = layout
    self.width      = width
    self.height     = height
    self.canvas     = draw.Drawing(self.width, self.height, origin="center")
    self.activities = []

  def render(self):
    for activity, pos in zip(self.activities, self.layout):
      self.canvas.append(
        self.shape.render(activity).at(pos)
      )
    return self

  def __str__(self):
    return self.canvas.as_svg()

@dataclass
class Activity:
  # bare minimum
  when              : datetime
  elapsed_time      : int
  distance          : float
  # optional
  calories          : Union[int,   None] = field(default=None)
  moving_time       : Union[int,   None] = field(default=None)
  max_heart_rate    : Union[int,   None] = field(default=None)
  avg_heart_rate    : Union[int,   None] = field(default=None)
  max_speed         : Union[float, None] = field(default=None)
  avg_speed         : Union[float, None] = field(default=None)
  avg_elapsed_speed : Union[float, None] = field(default=None)
  elevation_gain    : Union[float, None] = field(default=None)
  elevation_loss    : Union[float, None] = field(default=None)
  elevation_low     : Union[float, None] = field(default=None)
  elevation_high    : Union[float, None] = field(default=None)
  max_cadence       : Union[int,   None] = field(default=None)
  avg_cadence       : Union[int,   None] = field(default=None)

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
