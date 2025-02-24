import gpxpy
import gpxpy.gpx
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import folium
import webview

# -----------------------------
# CONFIGURATION
# -----------------------------
file_path = "maple_leaf_simple_path.csv"
scale_factor = 0.1  # Adjust route size
reference_latitude = 43.66304
reference_longitude = -79.30567
time_increment = timedelta(seconds=60)  # 1 minute between points
window_width = 800
window_height = 500

# -----------------------------
# LOAD CSV AND PROCESS COORDINATES
# -----------------------------
df = pd.read_csv(file_path)
anchor = df.loc[df["Label"].str.contains("Stem Lower Right 1", case=False, na=False)]
anchor_x, anchor_y = anchor.iloc[0]["X"], anchor.iloc[0]["Y"]

# Conversion factors
km_to_latitude = 111.32
km_to_longitude = 111.32 * np.cos(np.radians(reference_latitude))

# Transform coordinates
df["Latitude"] = reference_latitude + ((df["Y"] - anchor_y) * scale_factor / km_to_latitude)
df["Longitude"] = reference_longitude + ((df["X"] - anchor_x) * scale_factor / km_to_longitude)

# -----------------------------
# 🗺️ CREATE GPX STRUCTURE
# -----------------------------
gpx = gpxpy.gpx.GPX()

# Create track
gpx_track = gpxpy.gpx.GPXTrack(name="Maple Leaf Track")
gpx.tracks.append(gpx_track)
gpx_segment = gpxpy.gpx.GPXTrackSegment()
gpx_track.segments.append(gpx_segment)

# Create route
gpx_route = gpxpy.gpx.GPXRoute(name="Maple Leaf Route")
gpx.routes.append(gpx_route)

# -----------------------------
# 📝 ADD TRACK AND ROUTE POINTS
# -----------------------------
start_time = datetime.utcnow()
points_for_map = []

for index, row in df.iterrows():
    lat, lon = row["Latitude"], row["Longitude"]
    elevation = round(74.0 + np.random.uniform(-0.5, 0.5), 1)  # Simulated elevation
    point_time = start_time + index * time_increment

    # Track point
    track_point = gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=elevation, time=point_time)
    gpx_segment.points.append(track_point)

    # Route point with cues
    if index == 0:
        cue_name, cue_text, cue_type = "Start", "Start of route", "depart"
    elif index == len(df) - 1:
        cue_name, cue_text, cue_type = "End", "Arrive at destination", "arrive"
    else:
        prev_row = df.iloc[index - 1]
        next_row = df.iloc[index + 1]
        prev_angle = np.arctan2(row["Latitude"] - prev_row["Latitude"], row["Longitude"] - prev_row["Longitude"])
        next_angle = np.arctan2(next_row["Latitude"] - row["Latitude"], next_row["Longitude"] - row["Longitude"])
        angle_diff = (np.degrees(next_angle - prev_angle) + 180) % 360 - 180  # Normalize [-180, 180]

        if angle_diff > 30:
            cue_name, cue_text, cue_type = "Right", f"Turn right onto {next_row['Label']}", "right"
        elif angle_diff < -30:
            cue_name, cue_text, cue_type = "Left", f"Turn left onto {next_row['Label']}", "left"
        else:
            cue_name, cue_text, cue_type = "Straight", f"Continue onto {next_row['Label']}", "straight"

    route_point = gpxpy.gpx.GPXRoutePoint(lat, lon, name=cue_name, comment=cue_text)
    route_point.sym = "Direction"
    route_point.type = "turn"
    route_point.desc = cue_text  # Add turn description here
    route_point.type = cue_type  # Set Garmin-recognized type

    gpx_route.points.append(route_point)

    # Collect points for the map
    points_for_map.append((lat, lon))

# -----------------------------
# 💾 SAVE GPX FILE
# -----------------------------
gpx_file = f"maple_leaf_{int(scale_factor * 100)}pct.gpx"
with open(gpx_file, "w") as f:
    f.write(gpx.to_xml())

print(f"GPX file saved as: {gpx_file}")

# -----------------------------
# 🌍 CREATE INTERACTIVE MAP
# -----------------------------
# Initialize map centered at the midpoint of the route
center_lat = df["Latitude"].mean()
center_lon = df["Longitude"].mean()
map_route = folium.Map(location=[center_lat, center_lon], zoom_start=15, width=800, height=500)

# Add route line
folium.PolyLine(points_for_map, color="red", weight=4, opacity=0.8, tooltip="Maple Leaf Route").add_to(map_route)

# Calculate padding to achieve ~50% route coverage of the smaller dimension
smaller_dimension = min(window_width, window_height)
padding_factor = (1 - 0.5) / 2  # 50% coverage means 25% padding on each side

# Calculate bounding box with padding
lat_min, lat_max = df["Latitude"].min(), df["Latitude"].max()
lon_min, lon_max = df["Longitude"].min(), df["Longitude"].max()

lat_padding = (lat_max - lat_min) * padding_factor
lon_padding = (lon_max - lon_min) * padding_factor

# Adjusted bounds
adjusted_bounds = [[lat_min - lat_padding, lon_min - lon_padding],
                   [lat_max + lat_padding, lon_max + lon_padding]]

# Fit the map to the adjusted bounds
map_route.fit_bounds(adjusted_bounds)


# Add start and end markers
folium.Marker(points_for_map[0], popup="Start", icon=folium.Icon(color="green")).add_to(map_route)
folium.Marker(points_for_map[-1], popup="End", icon=folium.Icon(color="red")).add_to(map_route)

# Fit the map bounds to the route with padding to achieve ~80% width usage
#map_route.fit_bounds([[df["Latitude"].min(), df["Longitude"].min()], [df["Latitude"].max(), df["Longitude"].max()]])

# Save map to HTML
map_file = f"maple_leaf_{int(scale_factor * 100)}pct_map.html"
map_route.save(map_file)
print(f"Interactive map saved as: {map_file}")

# Open in popup window (500x800)
webview.create_window("Maple Leaf Route", map_file, width=800, height=500)
webview.start()