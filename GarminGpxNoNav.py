import gpxpy
import gpxpy.gpx
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load CSV file
file_path = "maple_leaf_simple_path.csv"
df = pd.read_csv(file_path)

# Set scale factor (e.g., 0.1 = 10%)
scale_factor = 0.1

# Find the "Stem Lower Right 1" point for anchor
anchor = df.loc[df["Label"].str.contains("Stem Lower Right 1", case=False, na=False)]
anchor_x, anchor_y = anchor.iloc[0]["X"], anchor.iloc[0]["Y"]

# Reference coordinates (Woodbine Beach)
reference_latitude = 43.66304
reference_longitude = -79.30567

# Scaling factors
km_to_latitude = 111.32  # degrees per km
km_to_longitude = 111.32 * np.cos(np.radians(reference_latitude))

# Apply coordinate transformation
df["Latitude"] = reference_latitude + ((df["Y"] - anchor_y) * scale_factor / km_to_latitude)
df["Longitude"] = reference_longitude + ((df["X"] - anchor_x) * scale_factor / km_to_longitude)

# Initialize GPX
gpx = gpxpy.gpx.GPX()

# Create Track
gpx_track = gpxpy.gpx.GPXTrack(name="Maple Leaf Track")
gpx.tracks.append(gpx_track)
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)

# Create Route
gpx_route = gpxpy.gpx.GPXRoute(name="Maple Leaf Route")
gpx.routes.append(gpx_route)

# Generate timestamps for track points
start_time = datetime.utcnow()
time_increment = timedelta(seconds=60)  # 1 minute between points

# Add track and route points
for index, row in df.iterrows():
    lat, lon = row["Latitude"], row["Longitude"]
    elevation = round(74.0 + np.random.uniform(-0.5, 0.5), 1)  # Simulated elevation
    point_time = start_time + index * time_increment

    # Add track point with elevation and time
    track_point = gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=elevation, time=point_time)
    gpx_segment.points.append(track_point)

    # Add route point with cues
    if index == 0:
        cue_name, cue_text = "Start", "Starting point"
    elif index == len(df) - 1:
        cue_name, cue_text = "End", "End of route"
    else:
        prev_row = df.iloc[index - 1]
        next_row = df.iloc[index + 1]
        prev_angle = np.arctan2(row["Latitude"] - prev_row["Latitude"], row["Longitude"] - prev_row["Longitude"])
        next_angle = np.arctan2(next_row["Latitude"] - row["Latitude"], next_row["Longitude"] - row["Longitude"])
        angle_diff = np.degrees(next_angle - prev_angle)
        angle_diff = (angle_diff + 180) % 360 - 180  # Normalize to [-180, 180]

        if angle_diff > 30:
            cue_name, cue_text = "Right", f"Turn right onto {next_row['Label']}"
        elif angle_diff < -30:
            cue_name, cue_text = "Left", f"Turn left onto {next_row['Label']}"
        else:
            cue_name, cue_text = "Straight", f"Continue onto {next_row['Label']}"

    route_point = gpxpy.gpx.GPXRoutePoint(lat, lon, name=cue_name, comment=cue_text)
    gpx_route.points.append(route_point)

# Save the GPX file
gpx_file = f"maple_leaf_{int(scale_factor * 100)}pct.gpx"
with open(gpx_file, "w") as f:
    f.write(gpx.to_xml())

print(f"GPX file saved as: {gpx_file}")
