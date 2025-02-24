import gpxpy
import gpxpy.gpx
import pandas as pd

# Load CSV
file_path = "maple_leaf_path.csv"
df = pd.read_csv(file_path)

# Create a GPX object
gpx = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)

# Convert X,Y to Latitude/Longitude for GPX format
for index, row in df.iterrows():
    gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(row["Y"], row["X"], name=row["Label"]))

# Save the GPX file
gpx_file = "maple_leaf_path.gpx"
with open(gpx_file, "w") as f:
    f.write(gpx.to_xml())

print(f"GPX file saved as: {gpx_file}")
