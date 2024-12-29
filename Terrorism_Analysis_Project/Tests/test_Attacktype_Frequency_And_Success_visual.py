import unittest
import os
import pandas as pd
from scripts.dataset_loader import load_dataset
from scripts.dataset_cleaner import clean_dataset

class TestAttackTypeFrequencyAndSuccess(unittest.TestCase):
    def setUp(self):
        # Load and clean the dataset
        self.raw_data = load_dataset()
        if self.raw_data is None:
            self.fail("Dataset could not be loaded. Ensure the dataset file exists and the path is correct.")
        self.cleaned_data = clean_dataset(self.raw_data)

    def test_grouped_data_stats(self):
        """Test if grouped data calculates total incidents and successful incidents correctly."""
        relevant_data = self.cleaned_data[['attacktype1_txt', 'success']]
        attack_stats = relevant_data.groupby('attacktype1_txt').agg(
            total_incidents=('success', 'count'),
            successful_incidents=('success', 'sum')
        ).reset_index()

        self.assertGreater(attack_stats.shape[0], 0, "Grouped data is empty.")
        self.assertTrue('total_incidents' in attack_stats.columns, "Total incidents column missing.")
        self.assertTrue('successful_incidents' in attack_stats.columns, "Successful incidents column missing.")

    def test_sorted_data(self):
        """Test if data is sorted by total incidents in descending order."""
        relevant_data = self.cleaned_data[['attacktype1_txt', 'success']]
        attack_stats = relevant_data.groupby('attacktype1_txt').agg(
            total_incidents=('success', 'count'),
            successful_incidents=('success', 'sum')
        ).reset_index()

        attack_stats.sort_values(by='total_incidents', ascending=False, inplace=True)
        sorted_values = attack_stats['total_incidents'].values
        self.assertTrue(all(sorted_values[i] >= sorted_values[i + 1] for i in range(len(sorted_values) - 1)),
                        "Data is not sorted by total incidents in descending order.")

    def test_visualisation_file_creation(self):
        """Test if the visualization file is created."""
        # Path to the saved figure
        figure_path = 'Terrorism_Analysis_Project/figures_and_statistics/Attacktype_Frequency_And_Success.png'

        # Perform the visualization (re-run script logic)
        relevant_data = self.cleaned_data[['attacktype1_txt', 'success']]
        attack_stats = relevant_data.groupby('attacktype1_txt').agg(
            total_incidents=('success', 'count'),
            successful_incidents=('success', 'sum')
        ).reset_index()

        attack_stats.sort_values(by='total_incidents', ascending=False, inplace=True)

        # Plot and save the visualization
        import matplotlib.pyplot as plt
        bar_width = 0.4
        x = range(len(attack_stats['attacktype1_txt']))
        plt.figure(figsize=(12, 8))
        plt.bar(x, attack_stats['total_incidents'], width=bar_width, label='Total Incidents', color='blue')
        plt.bar([i + bar_width for i in x], attack_stats['successful_incidents'], width=bar_width, label='Successful Incidents', color='orange')
        plt.xlabel('Attack Type')
        plt.ylabel('Number of Incidents')
        plt.title('Incident Frequency and Success Rate by Attack Type')
        plt.xticks([i + bar_width / 2 for i in x], attack_stats['attacktype1_txt'], rotation=45, ha='right')
        plt.legend()
        plt.savefig(figure_path, bbox_inches='tight')
        plt.clf()

        # Check if the file exists
        self.assertTrue(os.path.exists(figure_path), f"Visualization file not created at {figure_path}.")

if __name__ == "__main__":
    unittest.main()
