# a first design consisting of circles along a Archimedean spiral

import math

import drawsvg as draw

from runposter import Shape, Layout

class Circle(Shape):
  def __init__(self, radius):
    super().__init__()
    self.radius = radius

  @property
  def circumradius(self):
    return self.radius

  @property
  def rendered(self):
    return draw.Circle(self.left, self.top, self.radius, fill="red")

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
