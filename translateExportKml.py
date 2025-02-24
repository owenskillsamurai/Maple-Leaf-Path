from simplekml import Kml
import pandas as pd

# === USER SETTINGS ===
scale_factor = 5  # Change this to adjust size (1 = 1km, 10 = 10km, etc.)

# Load the CSV file
file_path = "maple_leaf_path.csv"
df = pd.read_csv(file_path)

# Define Toronto reference point (Nathan Phillips Square)
reference_latitude = 43.6529  # Latitude of (0,0)
reference_longitude = -79.3849  # Longitude of (0,0)
#  Eglinton & Laird
reference_latitude = 43.713138
reference_longitude = -79.367231

# Scaling factors (adjusted per km in Toronto)
km_to_longitude = 0.013  # Approximate longitude degrees per km in Toronto
km_to_latitude = 0.009   # Approximate latitude degrees per km in Toronto

# Create a KML object
kml = Kml()

# Convert X,Y to real-world Latitude/Longitude
for index, row in df.iterrows():
    lat = reference_latitude + (row["Y"] * km_to_latitude * scale_factor)
    lon = reference_longitude + (row["X"] * km_to_longitude * scale_factor)
    kml.newpoint(name=row["Label"], coords=[(lon, lat)])

# Save the KML file
kml_file = f"maple_leaf_path_{scale_factor}km.kml"
kml.save(kml_file)

print(f"KML file saved as: {kml_file}")

