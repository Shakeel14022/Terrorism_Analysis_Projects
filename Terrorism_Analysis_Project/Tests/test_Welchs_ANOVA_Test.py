import unittest
import os
import pandas as pd
from pingouin import welch_anova
from scripts.dataset_loader import load_dataset
from scripts.dataset_cleaner import clean_dataset

class TestWelchsANOVA(unittest.TestCase):
    def setUp(self):
        # Load and clean the dataset
        self.raw_data = load_dataset()
        if self.raw_data is None:
            self.fail("Dataset could not be loaded. Ensure the dataset file exists and the path is correct.")
        self.cleaned_data = clean_dataset(self.raw_data)

    def test_filtered_data_not_empty(self):
        """Test if the filtered data for Welch's ANOVA is not empty."""
        filtered_data = self.cleaned_data[['nkill', 'attacktype1_txt']].dropna()
        self.assertGreater(filtered_data.shape[0], 0, "Filtered data is empty after removing missing values.")

    def test_welch_anova_results(self):
        """Test if Welch's ANOVA returns valid results."""
        filtered_data = self.cleaned_data[['nkill', 'attacktype1_txt']].dropna()
        welch_results = welch_anova(data=filtered_data, dv='nkill', between='attacktype1_txt')

        self.assertFalse(welch_results.empty, "Welch ANOVA results are empty.")
        
        # Updated: Check for actual columns returned by Welch's ANOVA
        expected_columns = ['Source', 'ddof1', 'ddof2', 'F', 'p-unc', 'np2']
        for column in expected_columns:
            self.assertIn(column, welch_results.columns, f"'{column}' column missing in Welch ANOVA results.")
        
        # Ensure important columns like 'F' and 'p-unc' have no null values
        self.assertTrue(welch_results['F'].notnull().all(), "Welch ANOVA 'F' column contains null values.")
        self.assertTrue(welch_results['p-unc'].notnull().all(), "Welch ANOVA 'p-unc' column contains null values.")

    def test_descriptive_statistics(self):
        """Test if descriptive statistics are calculated correctly."""
        filtered_data = self.cleaned_data[['nkill', 'attacktype1_txt']].dropna()
        desc_stats = filtered_data.groupby('attacktype1_txt')['nkill'].agg(['count', 'mean', 'std']).round(2)

        self.assertFalse(desc_stats.empty, "Descriptive statistics are empty.")
        self.assertIn('count', desc_stats.columns, "'count' column missing in descriptive statistics.")
        self.assertIn('mean', desc_stats.columns, "'mean' column missing in descriptive statistics.")
        self.assertIn('std', desc_stats.columns, "'std' column missing in descriptive statistics.")

    def test_statistics_file_update(self):
        """Test if results are appended to the statistics.txt file."""
        # Path to the statistics.txt file
        statistics_file = 'Terrorism_Analysis_Project/figures_and_statistics/statistics.txt'

        # Ensure file exists before test
        if not os.path.exists(statistics_file):
            with open(statistics_file, 'w') as f:
                f.write("--- Statistics File ---\n")

        # Perform Welch's ANOVA and append results
        filtered_data = self.cleaned_data[['nkill', 'attacktype1_txt']].dropna()
        welch_results = welch_anova(data=filtered_data, dv='nkill', between='attacktype1_txt')
        desc_stats = filtered_data.groupby('attacktype1_txt')['nkill'].agg(['count', 'mean', 'std']).round(2)

        with open(statistics_file, 'a') as f:
            f.write("\n--- Descriptive Statistics by Attack Type ---\n")
            f.write(desc_stats.to_string(index=True))
            f.write("\n\n--- Welch ANOVA Results ---\n")
            f.write(welch_results.to_string(index=False))
            f.write("\n")

        # Check if statistics were appended
        with open(statistics_file, 'r') as f:
            content = f.read()
        self.assertIn("--- Welch ANOVA Results ---", content, "Welch ANOVA results were not appended to statistics.txt.")
        self.assertIn("--- Descriptive Statistics by Attack Type ---", content, "Descriptive statistics were not appended to statistics.txt.")

if __name__ == "__main__":
    unittest.main()
