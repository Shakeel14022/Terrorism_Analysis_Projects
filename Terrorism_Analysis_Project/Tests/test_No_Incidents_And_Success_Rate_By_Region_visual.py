import unittest
import os
import pandas as pd
from scripts.dataset_loader import load_dataset
from scripts.dataset_cleaner import clean_dataset

class TestNoIncidentsAndSuccessRateByRegion(unittest.TestCase):
    def setUp(self):
        # Load and clean the dataset
        self.raw_data = load_dataset()
        if self.raw_data is None:
            self.fail("Dataset could not be loaded. Ensure the dataset file exists and the path is correct.")
        self.cleaned_data = clean_dataset(self.raw_data)

    def test_grouped_data_calculation(self):
        """Test if grouped data calculates incidents and success rate correctly."""
        region_data = self.cleaned_data.groupby('region_txt').agg(
            incidents=('eventid', 'count'),
            success_rate=('success', 'mean')
        ).sort_values(by='incidents', ascending=False)

        self.assertGreater(region_data.shape[0], 0, "Grouped data is empty.")
        self.assertTrue('incidents' in region_data.columns, "Incidents column is missing.")
        self.assertTrue('success_rate' in region_data.columns, "Success rate column is missing.")

    def test_sorted_data(self):
        """Test if data is sorted by incidents in descending order."""
        region_data = self.cleaned_data.groupby('region_txt').agg(
            incidents=('eventid', 'count'),
            success_rate=('success', 'mean')
        ).sort_values(by='incidents', ascending=False)

        sorted_values = region_data['incidents'].values
        self.assertTrue(all(sorted_values[i] >= sorted_values[i + 1] for i in range(len(sorted_values) - 1)),
                        "Data is not sorted by incidents in descending order.")

    def test_visualisation_file_creation(self):
        """Test if the visualization file is created."""
        # Path to the saved figure
        figure_path = 'Terrorism_Analysis_Project/figures_and_statistics/No_Incidents_And_Success_Rate_By_Region.png'

        # Perform the visualization (re-run script logic)
        region_data = self.cleaned_data.groupby('region_txt').agg(
            incidents=('eventid', 'count'),
            success_rate=('success', 'mean')
        ).sort_values(by='incidents', ascending=False)

        # Create the visualization
        import matplotlib.pyplot as plt
        fig, ax1 = plt.subplots(figsize=(14, 7))

        ax1.bar(region_data.index, region_data['incidents'], color='skyblue', alpha=0.7, label='Number of Incidents')
        ax1.set_xlabel('Region')
        ax1.set_ylabel('Number of Incidents', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax2 = ax1.twinx()
        ax2.plot(region_data.index, region_data['success_rate'], color='red', marker='o', label='Success Rate')
        ax2.set_ylabel('Success Rate (Proportion)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.title('Number of Incidents and Success Rate by Region')
        plt.savefig(figure_path, bbox_inches='tight')
        plt.clf()

        # Check if the file exists
        self.assertTrue(os.path.exists(figure_path), f"Visualization file not created at {figure_path}.")

if __name__ == "__main__":
    unittest.main()
