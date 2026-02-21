from runposter.sources.strava import Strava

def select(name):
  """
  factory function to dynamically select a module representing a source
  """
  return {
    "strava" : Strava
  }[name.lower()]
