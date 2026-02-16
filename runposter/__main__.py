import os

import pandas as pd

from datetime import datetime

from rich.console   import Console
from rich.logging   import RichHandler
from rich.traceback import install

from runposter         import Canvas
from runposter         import spiraling_circles as design
from runposter.sources import Strava

import logging

console = Console(stderr=True)

FORMAT="%(message)s"
DATEFMT="[%X]"
logging.basicConfig(
  level=os.environ.get("LOG_LEVEL", "INFO"),
  format=FORMAT, datefmt=DATEFMT,
  handlers=[RichHandler(console=console)]
)

logger = logging.getLogger("runposter")

# install(show_locals=True)

class RunPoster:
  def render(self, filename, year=datetime.today().year):
    logger.info(f"loading from '{filename}'")
    year = int(year)
    logger.info(f"filtering for '{year}'")

    # read Strava activities.csv from commandline argument
    df = pd.read_csv(filename)

    # select runs
    df = df[df[Strava.props()["type"]] == "Run"]

    when = Strava.props()["when"]
    # localize datetime
    df[when] = pd.to_datetime(df[when], utc=True)
    df[when] = df[when].dt.tz_convert("Europe/Brussels")
    # filter year
    df = df[df[when].dt.year == year]
    # ensure sorted by date
    df.sort_values(by=when, inplace=True)

    canvas = Canvas(design.Arcs(22), design.Spiral(22), Strava)
    return canvas.render(df)

if __name__ == "__main__":
  from fire import Fire
  Fire(RunPoster(), name="runposter")
