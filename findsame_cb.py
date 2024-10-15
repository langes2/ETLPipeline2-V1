import os
import pandas as pd

# Directory where the files are stored
directory = r"C:\Users\Public\Documents\ChargeBreakdowns"

# Function to get the most recently modified file
def get_latest_file(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

# Get the latest file
latest_file = get_latest_file(directory)
print(f"Processing file: {latest_file}")

# Read the CSV file without a header
df = pd.read_csv(latest_file, header=None)

# Create a new column that is a tuple of the first three columns
df['triple'] = list(zip(df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]))

# Find rows with duplicate triples and get the count of occurrences
duplicate_counts = df['triple'].value_counts()

# Iterate over the duplicate rows and modify column 2 for repeated values
for triple, count in duplicate_counts.items():
    if count > 1:
        # Find all rows where this triple occurs
        duplicate_rows = df[df['triple'] == triple]
        # Iterate over the duplicate rows and append " #<occurrence number>" to column 2
        for i, (index, row) in enumerate(duplicate_rows.iterrows(), start=1):
            df.at[index, df.columns[1]] = f"{row[1]} #{i}"

# Drop the 'triple' column (no longer needed)
df = df.drop(columns=['triple'])

# Overwrite the file without writing the header or the index
df.to_csv(latest_file, index=False, header=False)

print(f"File '{latest_file}' has been overwritten with the updated data without a header.")