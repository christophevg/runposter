# for now only Strava, yet let's be open to others ;-)

from runposter import ActivityFactory, Mapping

class Strava(ActivityFactory):
  """
  transformator mapping Strava activities to more abstract Activity instances
  """
  mapping = {
    "Activity Type"         : Mapping("type"),
    "Activity Date"         : Mapping("when"),
    "Calories"              : Mapping("calories"),
    "Elapsed Time"          : Mapping("elapsed_time"),
    "Distance.1"            : Mapping("distance"),
    "Max Heart Rate"        : Mapping("max_heart_rate", max=184),
    "Average Heart Rate"    : Mapping("avg_heart_rate", max=184),
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
