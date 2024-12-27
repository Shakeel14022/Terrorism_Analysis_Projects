import unittest
import pandas as pd
from scripts.dataset_loader import load_dataset
from scripts.dataset_cleaner import clean_dataset

class TestDatasetCleanerWithActualData(unittest.TestCase):
    def setUp(self):
        # Load the actual dataset
        self.raw_data = load_dataset()
        if self.raw_data is None:
            self.fail("Dataset could not be loaded. Ensure the dataset file exists and the path is correct.")

    def test_cleaning_removes_missing_rows(self):
        """Test if rows with missing critical numeric values are removed."""
        cleaned_data = clean_dataset(self.raw_data)
        self.assertGreater(cleaned_data.shape[0], 0, "All rows were removed during cleaning.")
        self.assertFalse(cleaned_data[['nkill', 'success']].isnull().any().any(), "Missing values in critical numeric columns were not handled.")

    def test_cleaning_fills_missing_text_columns(self):
        """Test if missing textual values are filled with 'Unknown'."""
        if self.raw_data[['attacktype1_txt', 'region_txt']].isnull().sum().sum() == 0:
            self.skipTest("No missing values in 'attacktype1_txt' or 'region_txt' to test filling with 'Unknown'.")
        cleaned_data = clean_dataset(self.raw_data)
        self.assertFalse(cleaned_data[['attacktype1_txt', 'region_txt']].isnull().any().any(), "Missing textual values were not handled.")
        if 'attacktype1_txt' in cleaned_data.columns:
            self.assertTrue((cleaned_data['attacktype1_txt'] == 'Unknown').sum() > 0, "'attacktype1_txt' missing values not filled with 'Unknown'.")
        if 'region_txt' in cleaned_data.columns:
            self.assertTrue((cleaned_data['region_txt'] == 'Unknown').sum() > 0, "'region_txt' missing values not filled with 'Unknown'.")

    def test_cleaning_numeric_conversion(self):
        """Test if numeric columns are converted to integers."""
        cleaned_data = clean_dataset(self.raw_data)
        numeric_columns = ['nkill', 'success', 'iyear', 'eventid']
        for column in numeric_columns:
            self.assertTrue(pd.api.types.is_integer_dtype(cleaned_data[column]), f"'{column}' is not integer type.")

    def test_cleaning_relevant_columns(self):
        """Test if only relevant columns are retained."""
        cleaned_data = clean_dataset(self.raw_data)
        expected_columns = ['nkill', 'success', 'attacktype1_txt', 'iyear', 'region_txt', 'eventid']
        self.assertListEqual(list(cleaned_data.columns), expected_columns, "Irrelevant columns were not removed.")

if __name__ == "__main__":
    unittest.main()
