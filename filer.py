import pandas as pd
import numpy as np

# Load the backup CSV file
input_file = "maple_leaf_path_bak.csv"  # Backup file
output_file = "maple_leaf_path.csv"     # New output file

# Read the CSV file
df = pd.read_csv(input_file).copy()

# Compute distances using Euclidean formula: d = sqrt((x2 - x1)^2 + (y2 - y1)^2)
def euclidean_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Create shifted columns for preceding and next points
df["X_prev"] = df["X"].shift(1).copy()
df["Y_prev"] = df["Y"].shift(1).copy()
df["X_next"] = df["X"].shift(-1).copy()
df["Y_next"] = df["Y"].shift(-1).copy()

# **Wrap-around logic** for closed polygon:
# First point: Distance from last point
df.loc[0, "X_prev"] = df.loc[len(df) - 1, "X"]
df.loc[0, "Y_prev"] = df.loc[len(df) - 1, "Y"]

# Last point: Distance to first point
df.loc[len(df) - 1, "X_next"] = df.loc[0, "X"]
df.loc[len(df) - 1, "Y_next"] = df.loc[0, "Y"]

# Calculate distances
df["Distance_From_Previous"] = df.apply(lambda row: euclidean_distance(row["X_prev"], row["Y_prev"], row["X"], row["Y"]), axis=1)
df["Distance_To_Next"] = df.apply(lambda row: euclidean_distance(row["X"], row["Y"], row["X_next"], row["Y_next"]), axis=1)

# Fill first and last points
df.loc[0, "Distance_From_Previous"] = euclidean_distance(df.loc[0, "X"], df.loc[0, "Y"], df.loc[len(df) - 1, "X"], df.loc[len(df) - 1, "Y"])
df.loc[len(df) - 1, "Distance_To_Next"] = euclidean_distance(df.loc[len(df) - 1, "X"], df.loc[len(df) - 1, "Y"], df.loc[0, "X"], df.loc[0, "Y"])

# Drop helper columns used for shifting
df.drop(columns=["X_prev", "Y_prev", "X_next", "Y_next"], inplace=True)

# Round all numeric values to 4 decimal places
df[["X", "Y", "Distance_From_Previous", "Distance_To_Next"]] = df[["X", "Y", "Distance_From_Previous", "Distance_To_Next"]].round(4)

# Reorder columns
df = df[["Label", "X", "Y", "Distance_From_Previous", "Distance_To_Next"]]

# Save to a new CSV file
df.to_csv(output_file, index=False)

print(f"Processed file saved as: {output_file}")
