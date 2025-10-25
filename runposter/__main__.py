import sys

import pandas as pd

from datetime import datetime

from runposter         import Canvas
from runposter         import spiraling_circles as design
from runposter.sources import Strava

filename = sys.argv[1]
if len(sys.argv) > 2:
  year = int(sys.argv[2])
else:
  year = datetime.today().year

# read Strava activities.csv from commandline argument
df = pd.read_csv(filename)

# select runs
df = df[df[Strava.prop["type"]] == "Run"]

when = Strava.prop["when"]
# localize datetime
df[when] = pd.to_datetime(df[when], utc=True)
df[when] = df[when].dt.tz_convert("Europe/Brussels")
# filter year
df = df[df[when].dt.year == year]

canvas = Canvas(design.Circle(22), design.Spiral(22))

# add activities
for activity in df.to_dict("records"):
  canvas.activities.append(Strava(activity))

print(canvas.render())
