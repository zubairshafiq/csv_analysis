import csv

# Open the CSV file in read-only mode.
# `newline=""` lets the csv module handle line endings consistently across platforms.

with open("sales_data.csv", "r", newline="") as file:
    # Build a CSV reader that parses each row into a list of column values.
    reader = csv.reader(file)

    # Read the first row from the file, which is expected to be the header row.
    # Using `next()` advances the iterator by one row without loading the full file.
    header = next(reader)

    # Print the header so we can verify available column names.
    print(header)
