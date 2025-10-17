# Student data as per the provided table
students = [
    {'hours': 2, 'pass': 0},
    {'hours': 4, 'pass': 0},
    {'hours': 6, 'pass': 1},
    {'hours': 8, 'pass': 1},
    {'hours': 10, 'pass': 1},
]

# Candidate split points (between each unique value)
split_points = [3, 5, 7, 9]

def gini(groups):
    total = sum(len(group) for group in groups)
    score = 0.0
    for group in groups:
        size = len(group)
        if size == 0:
            continue
        proportion_pass = sum(row['pass'] for row in group) / size
        proportion_fail = 1 - proportion_pass
        score += size / total * (1.0 - (proportion_pass ** 2 + proportion_fail ** 2))
    return score

# Try each split and print Gini impurities
best_split = None
best_gini = 1.0
for split in split_points:
    left = [row for row in students if row['hours'] <= split]
    right = [row for row in students if row['hours'] > split]
    impurity = gini([left, right])
    print(f"Split at {split:2d}: Gini = {impurity:.4f}")
    if impurity < best_gini:
        best_gini = impurity
        best_split = split

# Output the best split and tree
print(f"\nBest split at Study Hours <= {best_split}:")
print(f"If Study Hours <= {best_split} -> 'Fail' (0)")
print(f"If Study Hours >  {best_split} -> 'Pass' (1)")
