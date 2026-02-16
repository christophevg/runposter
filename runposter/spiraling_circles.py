# a first design consisting of circles along a Archimedean spiral

import math

import drawsvg as draw

from runposter import Shape, Layout

import logging
logger = logging.getLogger(__name__)

class Circle(Shape):
  def __init__(self, radius, fill, stroke="red", stroke_width=0):
    super().__init__()
    self.radius       = radius
    self.fill         = fill
    self.stroke       = stroke
    self.stroke_width = stroke_width

  @property
  def circumradius(self):
    return self.radius

  @property
  def rendered(self):
    return draw.Circle(self.left, self.top, self.radius, fill=self.fill)

class Arc(Circle):
  def __init__(self, radius, start, stop, *args, **kwargs):
    kwargs["fill"]         = kwargs.get("fill", "none")
    kwargs["stroke_width"] = kwargs.get("stroke_width", 4)
    super().__init__(radius, *args, **kwargs)
    self.start = start
    self.stop  = stop

  @property
  def rendered(self):
    return draw.Path(
      stroke=self.stroke, stroke_width=self.stroke_width, fill=self.fill
    ).arc(
      self.left, self.top, self.radius, self.start, self.stop
    )

class Arcs(Shape):
  statistics = [ "distance", "avg_speed", "avg_heart_rate" ]
  strokes = [ "blue", "green", "red" ]

  def __init__(self, radius, stroke_width=4):
    self.radius = radius
    self.stroke_width = stroke_width

  @property
  def rendered(self):
    g = draw.Group(fill="none")
    radius = self.radius
    start = 0
    for idx, statistic in enumerate(self.statistics):
      size = 359.99 * self.activity[statistic].pct
      logger.debug(f"{size} > 350 : {size>350}")
      arc = Arc(
        radius, start, size,
        stroke=self.strokes[idx],
        stroke_width=self.stroke_width)
      g.append(arc.at((self.left, self.top)))
      radius -= self.stroke_width
      start = 0
    return g

class Spiral(Layout):
  def __init__(self, circumradius, fa=2.1, fds=4):
    super().__init__(circumradius)
    self.a     = self.circumradius / fa
    self.ds    = self.circumradius / fds
    self.theta  = 0

  def __iter__(self):
    while True:
      yield (
        self.a * self.theta * math.cos(self.theta),
        self.a * self.theta * math.sin(self.theta)
      )
      # prepare next
      # credits: https://math.stackexchange.com/a/2216736
      dt = self.ds / math.sqrt(1 + self.theta**2)
      self.theta += dt
