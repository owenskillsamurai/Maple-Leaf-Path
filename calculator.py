import pandas as pd

# Load the dataset
file_path = "maple_leaf_path.csv"  # Ensure this is the correct file
df = pd.read_csv(file_path)

# Calculate width and height
width_km = df["X"].max() - df["X"].min()
height_km = df["Y"].max() - df["Y"].min()

# Calculate total perimeter distance
total_distance_km = df["Distance_From_Previous"].sum()

# Print results
print(f"Width of the maple leaf: {width_km:.4f} km")
print(f"Height of the maple leaf: {height_km:.4f} km")
print(f"Total path distance (perimeter): {total_distance_km:.4f} km")
