import os
import pandas as pd

def get_most_recent_file(directory):
    # Get all files in the specified directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # If there are no files, return None
    if not files:
        return None

    # Get the most recently modified file
    most_recent_file = max(files, key=os.path.getmtime)
    
    return most_recent_file

def process_csv_in_place(file_path):
    # Load the CSV file without headers into a DataFrame
    df = pd.read_csv(file_path, header=None)
    
    # Step 1: Fill blanks in the first column by copying the data from the cell above
    df.iloc[:, 0] = df.iloc[:, 0].fillna(method='ffill')
    
    # Step 2: Take the 20-character suffix of the first row, first column
    first_row_suffix = str(df.iloc[0, 0])[-20:]
    
    # Step 3: Append the suffix to all rows in the first column, if not already present
    def append_suffix_if_not_present(value):
        str_value = str(value)
        if not str_value.endswith(first_row_suffix):
            return str_value + first_row_suffix
        return str_value
    
    df.iloc[:, 0] = df.iloc[:, 0].apply(append_suffix_if_not_present)
    
    # Step 4: Delete the first row
    df = df.drop(index=0).reset_index(drop=True)
    
    # Step 5: Remove rows where the second column is blank
    df = df.dropna(subset=[1])
    
    # Overwrite the original file without a header
    df.to_csv(file_path, header=False, index=False)

def modify_recent_file_in_directory(directory):
    # Get the most recently modified file in the directory
    recent_file = get_most_recent_file(directory)
    
    if recent_file:
        print(f"Processing the most recent file: {recent_file}")
        process_csv_in_place(recent_file)
    else:
        print("No files found in the specified directory.")

# Usage:
directory = r"C:\Users\Public\Documents\ChargeBreakdowns"
modify_recent_file_in_directory(directory)