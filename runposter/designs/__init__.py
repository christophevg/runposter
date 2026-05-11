from runposter.designs.spiraling_circles import Arcs, Circle, Segments, Spiral


def select_layout(name, *args, **kwargs):
  """
  factory function to dynamically select a layout class
  """
  return {
    "spiral" : Spiral
  }[name.lower()](*args, **kwargs)

def select_shape(name, *args, **kwargs):
  """
  factory function to dynamically select a shape class
  """
  return {
    "circle"   : Circle,
    "arcs"     : Arcs,
    "segments" : Segments
  }[name.lower()](*args, **kwargs)
