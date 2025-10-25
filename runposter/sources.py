# for now only Strava, yet let's be open to others ;-)

from runposter import Activity

class Strava(Activity):
  """
  transformator mapping Strava activities to more abstract Activity instances
  """
  mapping = {
    "Activity Date"         : "when",
    "Calories"              : "calories",
    "Elapsed Time"          : "elapsed_time",
    "Distance.1"            : "distance",
    "Max Heart Rate"        : "max_heart_rate",
    "Average Heart Rate"    : "avg_heart_rate",
    "Moving Time"           : "moving_time",
    "Max Speed"             : "max_speed",
    "Average Speed"         : "avg_speed",
    "Average Elapsed Speed" : "avg_elapsed_speed",
    "Elevation Gain"        : "elevation_gain",
    "Elevation Loss"        : "elevation_loss",
    "Elevation Low"         : "elevation_low",
    "Elevation High"        : "elevation_high",
    "Max Cadence"           : "max_cadence",
    "Average Cadence"       : "avg_cadence"
  }
  cols = list(mapping.keys())
  prop = { v:k for k,v in mapping.items() }
  prop["type"] = "Activity Type"

  def __init__(self, activity):
    super().__init__(
      **{trg : activity[src] for src, trg in self.mapping.items()}
    )
