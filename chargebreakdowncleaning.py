import pandas as pd
import os
import glob

def modify_excel_file(input_file):
    # Load the Excel file
    df = pd.read_excel(input_file, header=None)
    
    # Drop the specified rows (row indices start from 0, so subtract 1)
    df = df.drop([0, 1, 3])

    # Drop the specified columns (column indices start from 0, so subtract 1)
    columns_to_drop = [2, 5, 7, 8, 12, 15, 18, 25]
    df = df.drop(df.columns[columns_to_drop], axis=1)

    # Find the row containing the phrase "Charge Breakdown (Summary)"
    phrase = "Charge Breakdown (Summary)"
    row_index = df[df.apply(lambda row: row.astype(str).str.contains(phrase, regex=False).any(), axis=1)].index
    
    if not row_index.empty:
        # Calculate the row from which to keep data
        cutoff_index = max(0, row_index[0] - 3)
        # Keep all rows up to three rows above the row with the phrase
        df = df[:cutoff_index]
    
    # Clean the DataFrame by applying the custom cleaning function
    df = clean_dataframe(df)
    
    # Save the modified and cleaned DataFrame to a CSV file without the header
    output_file = os.path.splitext(input_file)[0] + '.csv'
    df.to_csv(output_file, index=False, header=False)
    
    # Delete the original Excel file
    os.remove(input_file)

def clean_dataframe(df):
    """
    Cleans the DataFrame by:
    1. Removing rows where both the first and second columns are blank or NaN.
    2. Removing rows where the first column contains "Property Total", "Property Counts", 
       "Overall Total", or "Overall Counts".
    
    Parameters:
    df (pandas.DataFrame): The DataFrame to be cleaned.
    
    Returns:
    pandas.DataFrame: The cleaned DataFrame.
    """
    # Drop rows where both the first and second columns are blank or NaN
    df_cleaned = df.dropna(subset=[df.columns[0], df.columns[1]], how='all')

    # Drop rows where the first column contains specific keywords
    keywords_to_remove = ['Property Total', 'Property Counts', 'Overall Total', 'Overall Counts']
    df_cleaned = df_cleaned[~df_cleaned[df.columns[0]].isin(keywords_to_remove)]

    return df_cleaned

def main():
    # Define the directory to search for Excel files
    directory = r"C:\Users\Public\Documents\ChargeBreakdowns"

    # Get the list of all Excel files in the directory, sorted by modification time
    list_of_files = glob.glob(os.path.join(directory, "*.xlsx"))
    latest_file = max(list_of_files, key=os.path.getmtime)

    # Modify the most recently modified file
    modify_excel_file(latest_file)

if __name__ == "__main__":
    main()
