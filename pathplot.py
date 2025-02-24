import pandas as pd
import matplotlib.pyplot as plt

# Load the coordinate data from CSV
file_path = "maple_leaf_path.csv"  # Change to your file path if needed
file_path = "maple_leaf_simple_path.csv"  # Change to your file path if needed
df = pd.read_csv(file_path)

# Extract X and Y values
x_vals = df["X"].values
y_vals = df["Y"].values
labels = df["Label"].values

# Create the plot
plt.figure(figsize=(6, 6))

# Scatter plot for vertices
plt.scatter(x_vals, y_vals, color="red", label="Vertices")  # Red dots for vertices

# Connect the points to form the maple leaf shape
plt.plot(x_vals, y_vals, linestyle="dashed", color="blue", alpha=0.7, label="Maple Leaf Shape")  # Blue dashed outline

# Wrap-around: Connect last point to first point to complete the polygon
plt.plot([x_vals[-1], x_vals[0]], [y_vals[-1], y_vals[0]], linestyle="dashed", color="blue", alpha=0.7)

# **Dynamic label placement with special handling for "Lower Left/Right Lateral Apex"**
for i, label in enumerate(labels):
    x, y = x_vals[i], y_vals[i]
    
    # **Custom placement for specific labels**
    if "Stem Lower" in label or "Lower Left Lateral Apex" in label or "Lower Right Lateral Apex" in label:
        va = "top"  # Force beloe
    elif "Apex" or "Upper" in label:
    #elif "Apex" in label:
        va = "bottom"  # Other Apex labels go above
    elif "Sinus" in label or "Lower Left Lateral Apex" in label or "Lower Right Lateral Apex" in label:
        va = "top"  # Sinus + Lower Apex labels go below
    else:
        va = "center"  # Default vertical alignment
    
    # Horizontal alignment rules
    if x > 0.9:  # If near the right boundary, force left alignment
        ha = "right"
    elif x < 0.1:  # If near the left boundary, force right alignment
        ha = "left"
    elif "Left" in label:
        ha = "right"
    elif "Right" in label:
        ha = "left"
    else:
        ha = "center"  # Default horizontal alignment

    
    # Add the text with adjusted placement
    plt.text(x, y, label, fontsize=8, ha=ha, va=va, fontweight="bold")
    
    # Add the text with adjusted placement
    plt.text(x, y, label, fontsize=8, ha=ha, va=va, fontweight="bold")

# Axis Labels and titles
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.title("Normalized Maple Leaf Outline")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
