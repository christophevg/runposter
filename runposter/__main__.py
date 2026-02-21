import os

from datetime import datetime

from rich.console   import Console
from rich.logging   import RichHandler

from runposter import Canvas, sources
from runposter import spiraling_circles as design

import logging

# load the environment variables for this setup
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
load_dotenv(".env.local")

console = Console(stderr=True)

FORMAT="%(message)s"
DATEFMT="[%X]"
logging.basicConfig(
  level=os.environ.get("LOG_LEVEL", "INFO"),
  format=FORMAT, datefmt=DATEFMT,
  handlers=[RichHandler(console=console)]
)

logger = logging.getLogger("runposter")

statistics = {
  "distance"      : "blue",
  "avg_speed"     : "green",
  "avg_heart_rate": "red",
  "moving_time"   : "yellow",
  "avg_cadence"   : "orange"
}

class RunPoster:
  def __init__(self):
    self.source = sources.select("Strava")
    self.layout = design.Spiral(21)
    self.shape  = design.Segments(statistics, 19.5)

  def from_source(self, name):
    """
    Sets up the source that the activities are obtained from. Possible values include "Strava".
    """
    self.source = sources.select(name)
    return self

  def render(self, filename, year=datetime.today().year, height=1189):
    year = int(year)

    # read activities from source as pandas df
    df = self.source.load(filename, only_year=year)

    canvas = Canvas(self.shape, self.layout, self.source, height=height)
    return canvas.render(df)

if __name__ == "__main__":
  from fire import Fire
  Fire(RunPoster(), name="runposter")
