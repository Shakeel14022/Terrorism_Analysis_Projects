import pandas as pd

def clean_dataset(data):
    
    # Cleans the dataset to remove inconsistencies and handle missing values.
      
    # Remove rows with all missing values
    data.dropna(how='all', inplace=True)

    # Remove rows with missing values in critical numerical columns
    critical_numeric_columns = ['nkill', 'success']
    data.dropna(subset=critical_numeric_columns, inplace=True)

    # Fill missing values in critical textual columns with 'Unknown'
    columns_to_fill = ['attacktype1_txt', 'region_txt']
    for column in columns_to_fill:
        if column in data.columns:
            data.loc[:, column] = data[column].fillna('Unknown')

    # Ensure all numeric columns have correct types
    numeric_columns = ['nkill', 'success', 'iyear', 'eventid']
    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(data[column], errors='coerce').fillna(0).astype(int)

    # Remove duplicate rows
    data.drop_duplicates(inplace=True)

    # Retain only relevant columns
    relevant_columns = ['nkill', 'success', 'attacktype1_txt', 'iyear', 'region_txt', 'eventid']
    data = data[relevant_columns]

    print("Dataset cleaning completed.")
    return data
