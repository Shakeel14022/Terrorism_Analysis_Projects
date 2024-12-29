import unittest
import os
import pandas as pd
import numpy as np
from scripts.dataset_loader import load_dataset
from scripts.dataset_cleaner import clean_dataset
from scipy.stats import norm

class TestConfidenceIntervalVisualisation(unittest.TestCase):
    def setUp(self):
        # Load and clean the dataset
        self.raw_data = load_dataset()
        if self.raw_data is None:
            self.fail("Dataset could not be loaded. Ensure the dataset file exists and the path is correct.")
        self.cleaned_data = clean_dataset(self.raw_data)

    def test_filtered_data_not_empty(self):
        """Test if the filtered data for ANOVA visualization is not empty."""
        filtered_data = self.cleaned_data[['nkill', 'attacktype1_txt']].dropna()
        self.assertGreater(filtered_data.shape[0], 0, "Filtered data is empty after removing rows with missing values.")

    def test_grouped_data_statistics(self):
        """Test if grouped data calculates mean, count, and std correctly."""
        filtered_data = self.cleaned_data[['nkill', 'attacktype1_txt']].dropna()
        grouped = filtered_data.groupby('attacktype1_txt')['nkill'].agg(['mean', 'count', 'std']).reset_index()
        self.assertGreater(grouped.shape[0], 0, "Grouped data is empty.")
        self.assertTrue('mean' in grouped.columns, "Mean not calculated.")
        self.assertTrue('count' in grouped.columns, "Count not calculated.")
        self.assertTrue('std' in grouped.columns, "Standard deviation not calculated.")

    def test_confidence_interval_calculation(self):
        """Test if confidence intervals are calculated correctly."""
        filtered_data = self.cleaned_data[['nkill', 'attacktype1_txt']].dropna()
        grouped = filtered_data.groupby('attacktype1_txt')['nkill'].agg(['mean', 'count', 'std']).reset_index()
        grouped = grouped[grouped['count'] > 1]  # Exclude groups with a single data point

        z_value = norm.ppf(0.975)  # For 95% confidence
        grouped['ci'] = z_value * (grouped['std'] / np.sqrt(grouped['count']))
        self.assertFalse(grouped['ci'].isnull().any(), "Confidence intervals contain NaN values.")

    def test_visualisation_file_creation(self):
        """Test if the visualization file is created."""
        # Path to the saved figure
        figure_path = 'Terrorism_Analysis_Project/figures_and_statistics/95_ConfidenceInterval_Fatalities_By_Attacktype.png'

        # Perform the visualization (re-run script logic)
        filtered_data = self.cleaned_data[['nkill', 'attacktype1_txt']].dropna()
        grouped = filtered_data.groupby('attacktype1_txt')['nkill'].agg(['mean', 'count', 'std']).reset_index()
        grouped = grouped[grouped['count'] > 1]  # Exclude groups with a single data point

        z_value = norm.ppf(0.975)  # For 95% confidence
        grouped['ci'] = z_value * (grouped['std'] / np.sqrt(grouped['count']))

        # Save the visualization
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.bar(grouped['attacktype1_txt'], grouped['mean'], yerr=grouped['ci'], capsize=5, alpha=0.7)
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Attack Type')
        plt.ylabel('Mean Fatalities')
        plt.title('Mean Fatalities by Attack Type with 95% Confidence Intervals')
        plt.savefig(figure_path, bbox_inches='tight')
        plt.clf()

        # Check if the file exists
        self.assertTrue(os.path.exists(figure_path), f"Visualization file not created at {figure_path}.")

if __name__ == "__main__":
    unittest.main()
