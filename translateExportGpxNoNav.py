import gpxpy
import gpxpy.gpx
import pandas as pd
import numpy as np

# Load CSV file
file_path = "maple_leaf_simple_path.csv"
df = pd.read_csv(file_path)

# **Set the Scale Factor Here**
scale_factor = 0.1  # Change this to adjust the size (e.g., 10 = 10km)

# Find the "Stem Lower Right 1" point explicitly from CSV
anchor = df.loc[df["Label"].str.contains("Stem Lower Right 1", case=False, na=False)]

# Get the (X, Y) coordinates of the Stem Lower Right 1 point
anchor_x, anchor_y = anchor.iloc[0]["X"], anchor.iloc[0]["Y"]

# Reference coordinates (Woodbine Beach as default)
reference_latitude = 43.66304
reference_longitude = -79.30567

# Scaling factors
km_to_latitude = 111.32   # Latitude degrees per km
km_to_longitude = 111.32 * np.cos(np.radians(reference_latitude))  # Adjust for latitude

# **Apply transformation to all points relative to "Stem Lower Right 1"**
df["Latitude"] = reference_latitude + ((df["Y"] - anchor_y) * scale_factor / km_to_latitude)
df["Longitude"] = reference_longitude + ((df["X"] - anchor_x) * scale_factor / km_to_longitude)

# Create a GPX object
gpx = gpxpy.gpx.GPX()
gpx_track = gpxpy.gpx.GPXTrack()
gpx.tracks.append(gpx_track)
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)

# **Convert Coordinates to GPX Format Without Navigation Cues**
for index, row in df.iterrows():
    lat, lon = row["Latitude"], row["Longitude"]
    point = gpxpy.gpx.GPXTrackPoint(lat, lon, name=row["Label"])
    gpx_segment.points.append(point)

# **Handle the start and end waypoints efficiently**
start_lat, start_lon = df.iloc[0]["Latitude"], df.iloc[0]["Longitude"]
end_lat, end_lon = df.iloc[-1]["Latitude"], df.iloc[-1]["Longitude"]

if (start_lat != end_lat) or (start_lon != end_lon):
    gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(start_lat, start_lon, name="Start of the Route"))
    gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(end_lat, end_lon, name="Maple Leaf Completed!"))
else:
    gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(start_lat, start_lon, name="Start & End of the Route"))

# Save the GPX file
gpx_file = f"maple_leaf_{int(scale_factor)}km_no_nav.gpx"
with open(gpx_file, "w") as f:
    f.write(gpx.to_xml())

print(f"GPX file saved as: {gpx_file}")
