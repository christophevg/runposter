# a first design consisting of circles along a Archimedean spiral

import math

import drawsvg as draw

from runposter import Layout, Shape


class Circle(Shape):
  """
  Test Shape, that simply draws a full circle. Doesn't take into account activities information.
  """
  def __init__(self, _, radius, fill, stroke="red", stroke_width=0):
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

class _Arc(Circle):
  """
  A variation of the basic `Circle` shape. This version accepts additional `start` and `stop` angles to construct an arc. Doesn't take into account activities information. Not to be used as an actual Shape. Used by `Arcs`.
  """
  def __init__(self, radius, start, stop, *args, **kwargs):
    kwargs["fill"]         = kwargs.get("fill", "none")
    kwargs["stroke_width"] = kwargs.get("stroke_width", 4)
    super().__init__(None, radius, *args, **kwargs)
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
  """
  Renders statistics using layered arcs.
  """
  def __init__(self, radius, stroke_width=4):
    super().__init__()
    self.radius = radius
    self.stroke_width = stroke_width

  def create_visual(self, statistic, index=0, color="red"):
    size = 359.99 * self.activity[statistic].pct
    radius = self.radius - (self.stroke_width * index)
    return _Arc(
      radius, 0, size,
      stroke=color, stroke_width=self.stroke_width
    )

class Segments(Shape):
  def __init__(self, radius=22.0, stroke_width=4):
    super().__init__()
    self.radius = radius
    self.stroke_width = stroke_width

  def create_visual(self, statistic, index=0, color="red"):
    size = self.radius * self.activity[statistic].pct
    width = 360 / len(self.statistics)
    start = width * index
    return _Arc(
      size, start, start+width,
      stroke=color, stroke_width=size
    )

class Spiral(Layout):
  def __init__(self, circumradius, fa=2.1, fds=4):
    super().__init__(circumradius)
    self.a     = self.circumradius / fa
    self.ds    = self.circumradius / fds
    self.theta  = 0

  def __iter__(self):
    """
    yields the angle and consecutive points along an archimedes spiral, evenly separated by a constant given distance. along with it
    """
    while True:
      yield (
        int(self.a * self.theta * math.cos(self.theta)),
        int(self.a * self.theta * math.sin(self.theta)),
        self.theta
      )
      # prepare next
      # credits: https://math.stackexchange.com/a/2216736
      dt = self.ds / math.sqrt(1 + self.theta**2)
      self.theta += dt
