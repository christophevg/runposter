import logging
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler

_ = load_dotenv(Path().resolve() / ".env.local")

from runposter import Canvas, designs, sources # noqa

console = Console(stderr=True)

FORMAT="%(message)s"
DATEFMT="[%X]"
logging.basicConfig(
  level=os.environ.get("LOG_LEVEL", "INFO"),
  format=FORMAT, datefmt=DATEFMT,
  handlers=[RichHandler(console=console)]
)

logger = logging.getLogger("runposter")

# configuration for shapes that render multiple statistics
statistics = {
  "segments" : {
    "distance"      : "blue",
    "avg_speed"     : "green",
    "avg_heart_rate": "red",
    "moving_time"   : "yellow",
    "avg_cadence"   : "orange"
  }
}

class RunPoster:
  def __init__(self):
    # setup with some defaults
    self.using_layout("spiral", 21)
    self.using_shape("segments", 19.5)
    self.from_source("Strava")

  def using_layout(self, name, arg):
    """
    Sets up the layout that will be used. The name determines the layout and a single argument is provided to the layout's constructor.
    """
    self.layout = designs.select_layout(name, arg)
    return self

  def using_shape(self, name, arg):
    """
    Sets up the shape that will be used. The name determines the shape and a single argument is provided to the shape's constructor.
    If the name of the shape has a statistics configuration, it is added.
    """
    self.shape = designs.select_shape(name)
    try:
      self.shape.statistics = statistics[name]
    except KeyError:
      pass
    return self

  def from_source(self, name):
    """
    Sets up the source that the activities are obtained from. Possible values include "Strava".
    """
    self.source = sources.select(name)
    return self

  def render(self, filename, year=None, height=1189):
    """
    Render all activities in the given source, for the given year.
    """
    if not year:
      year = datetime.today().year
    year = int(year)

    # read activities from source as pandas df
    df = self.source.load(filename, only_year=year)

    logger.debug(f"loaded\n{df}")

    canvas = Canvas(self.shape, self.layout, self.source, height=height)
    return canvas.render(df)

if __name__ == "__main__":
  from fire import Fire
  Fire(RunPoster(), name="runposter")
