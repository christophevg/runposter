# for now only Strava, yet let's be open to others ;-)

import logging
import os

import pandas as pd

from runposter import ActivityFactory, Mapping

logger = logging.getLogger(__name__)

MAX_HR = int(os.environ.get("MAX_HR", 0))
if MAX_HR:
  logger.info(f"♥️ MAX_HR={MAX_HR}")

class Strava(ActivityFactory):
  """
  Factory loading and producing generic activities from Strava activities data.
  """
  mapping = {
    "Activity Type"         : Mapping("type"),
    "Activity Date"         : Mapping("when"),
    "Calories"              : Mapping("calories"),
    "Elapsed Time"          : Mapping("elapsed_time"),
    "Distance.1"            : Mapping("distance"),
    "Max Heart Rate"        : Mapping("max_heart_rate", max=MAX_HR),
    "Average Heart Rate"    : Mapping("avg_heart_rate", max=MAX_HR),
    "Moving Time"           : Mapping("moving_time"),
    "Max Speed"             : Mapping("max_speed"),
    "Average Speed"         : Mapping("avg_speed"),
    "Average Elapsed Speed" : Mapping("avg_elapsed_speed"),
    "Elevation Gain"        : Mapping("elevation_gain"),
    "Elevation Loss"        : Mapping("elevation_loss"),
    "Elevation Low"         : Mapping("elevation_low"),
    "Elevation High"        : Mapping("elevation_high"),
    "Max Cadence"           : Mapping("max_cadence"),
    "Average Cadence"       : Mapping("avg_cadence")
  }

  @classmethod
  def load(cls, filename, only_year=None):
    """
    Given the file path to an `activities.csv` file containing Strava activities, the function loads the activities, selects runs, localizes the activity date and optionally filters out activities for a specific year. Finally, it sorts the activities based on the activity date, returning a Pandas df, ready for further processing.
    """

    logger.info(f"loading from '{filename}'")
        # read activities.csv
    df = pd.read_csv(filename)

    # select runs
    df = df[df["Activity Type"] == "Run"]

    # localize datetime
    df["Activity Date"] = pd.to_datetime(df["Activity Date"], utc=True)
    df["Activity Date"] = df["Activity Date"].dt.tz_convert("Europe/Brussels")

    if only_year:
      logger.info(f"filtering for '{only_year}'")
      # filter year
      df = df[df["Activity Date"].dt.year == only_year]

    # ensure sorted by date
    df.sort_values(by="Activity Date", inplace=True)

    return df
