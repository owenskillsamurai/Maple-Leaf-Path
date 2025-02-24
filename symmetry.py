import pandas as pd

# Load the dataset
file_path = "maple_leaf_simple_path.csv"
df = pd.read_csv(file_path)

# Define corresponding left-right pairs
symmetry_pairs = [
    ("Primary Left Lobe Sinus", "Primary Right Lobe Sinus"),
    ("Primary Left Lobe Apex", "Primary Right Lobe Apex"),
    ("Primary Left Sinus", "Primary Right Sinus"),
    ("Upper Left Lateral Apex", "Upper Right Lateral Apex"),
    ("Upper Left Sinus", "Upper Right Sinus"),
    ("Left Lateral Apex", "Right Lateral Apex"),
    ("Lower Left Sinus", "Lower Right Sinus"),        
    ("Lower Left Lateral Apex", "Lower Right Lateral Apex"),
    ("Shoulder Left Sinus", "Shoulder Right Sinus"),
    ("Shoulder Left", "Shoulder Right"),
    ("Stem Upper Left", "Stem Upper Right"),
    ("Stem Lower Left", "Stem Lower Right 1"),
    ("Stem Lower Left", "Stem Lower Right    & 2")  
]

# Define the X-axis midpoint
X_CENTER = 0.5

# Check for symmetry issues
y_symmetry_issues = []
x_symmetry_issues = []

for left_label, right_label in symmetry_pairs:
    left_x = df.loc[df["Label"] == left_label, "X"].values
    right_x = df.loc[df["Label"] == right_label, "X"].values
    left_y = df.loc[df["Label"] == left_label, "Y"].values
    right_y = df.loc[df["Label"] == right_label, "Y"].values

    if len(left_y) == 1 and len(right_y) == 1:
        if abs(left_y[0] - right_y[0]) > 0.0001:  # Allow small floating-point differences
            y_symmetry_issues.append((left_label, right_label, left_y[0], right_y[0]))

    if len(left_x) == 1 and len(right_x) == 1:
        left_dist = abs(left_x[0] - X_CENTER)
        right_dist = abs(right_x[0] - X_CENTER)
        delta = left_dist - right_dist  # Always subtract right from left

        if abs(delta) > 0.0001:  # Allow small floating-point differences
            x_symmetry_issues.append((left_label, right_label, left_x[0], right_x[0], left_dist, right_dist, delta))


# Check that "Primary Apex" is exactly at X = 0.5
primary_apex_x = df.loc[df["Label"] == "Primary Apex", "X"].values
primary_apex_issue = None
if len(primary_apex_x) == 1:
    if abs(primary_apex_x[0] - X_CENTER) > 0.0001:
        primary_apex_issue = primary_apex_x[0]

# Print results
if y_symmetry_issues:
    print("Y-Symmetry Check Failed! These pairs have mismatched Y-values:")
    for left, right, y_left, y_right in y_symmetry_issues:
        print(f"{left} (Y={y_left:.4f}) != {right} (Y={y_right:.4f})")
else:
    print("Y-Symmetry Check Passed!")

# Print results
if x_symmetry_issues:
    print("\nX-Symmetry Check Failed! These pairs are not mirrored correctly around X=0.5:")
    for left, right, x_left, x_right, left_dist, right_dist, delta in x_symmetry_issues:
        print(f"{left} (X={x_left:.4f}) != {right} (X={x_right:.4f}), Left Dist: {left_dist:.4f}, Right Dist: {right_dist:.4f}, Delta: {delta:.4f}")
else:
    print("\nX-Symmetry Check Passed!")

if primary_apex_issue is not None:
    print(f"\nPrimary Apex is not centered! X={primary_apex_issue:.4f} (Expected: 0.5)")
else:
    print("\nPrimary Apex is correctly centered at X=0.5")
