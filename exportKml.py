from simplekml import Kml
import pandas as pd

# Load the CSV file
file_path = "maple_leaf_path.csv"  # Ensure this is the correct file
df = pd.read_csv(file_path)

# Create a KML object
kml = Kml()

# Convert X,Y to Latitude/Longitude for Google Maps
# Assuming X represents Longitude and Y represents Latitude in Toronto
for index, row in df.iterrows():
    kml.newpoint(name=row["Label"], coords=[(row["X"], row["Y"])])

# Save the KML file
kml_file = "maple_leaf_path.kml"
kml.save(kml_file)

print(f"KML file saved as: {kml_file}")
