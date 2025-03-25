my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Define slices (start, stop, step)
slices = [(0,0),(0, 3), (4, 7), (6, 9)]  # (inclusive start, exclusive stop)

# Extract slices
extracted_slices = [my_list[start:stop] for start, stop in slices]

print(extracted_slices)
