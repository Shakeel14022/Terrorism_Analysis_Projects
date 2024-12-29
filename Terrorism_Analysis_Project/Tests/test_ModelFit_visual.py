import unittest
import os
import pandas as pd
import numpy as np
from scripts.dataset_loader import load_dataset
from scripts.dataset_cleaner import clean_dataset

class TestModelFitVisualisation(unittest.TestCase):
    def setUp(self):
        # Load and clean the dataset
        self.raw_data = load_dataset()
        if self.raw_data is None:
            self.fail("Dataset could not be loaded. Ensure the dataset file exists and the path is correct.")
        self.cleaned_data = clean_dataset(self.raw_data)

    def test_yearly_data_aggregation(self):
        """Test if yearly data aggregation works correctly."""
        yearly_data = self.cleaned_data.groupby('iyear')['nkill'].sum().reset_index()
        self.assertGreater(yearly_data.shape[0], 0, "Yearly data aggregation is empty.")
        self.assertTrue('iyear' in yearly_data.columns, "'iyear' column missing after aggregation.")
        self.assertTrue('nkill' in yearly_data.columns, "'nkill' column missing after aggregation.")

    def test_exponential_model_fit(self):
        """Test if exponential model parameters are computed correctly."""
        yearly_data = self.cleaned_data.groupby('iyear')['nkill'].sum().reset_index()

        # Extract year (X) and total fatalities (y)
        X = yearly_data['iyear'].values
        y = yearly_data['nkill'].values

        # Normalize year for numerical stability
        X_normalised = X - 1970

        # Log-transform fatalities for linear regression
        log_y = np.log(y)

        # Perform linear regression
        X_with_intercept = np.c_[np.ones(X_normalised.shape[0]), X_normalised]
        beta = np.linalg.inv(X_with_intercept.T @ X_with_intercept) @ X_with_intercept.T @ log_y

        # Extract parameters
        ln_a = beta[0]
        b = beta[1]
        a = np.exp(ln_a)

        # Check if parameters are finite
        self.assertTrue(np.isfinite(a), "Parameter 'a' is not finite.")
        self.assertTrue(np.isfinite(b), "Parameter 'b' is not finite.")

    def test_visualisation_file_creation(self):
        """Test if the visualization file is created."""
        # Path to the saved figure
        figure_path = 'Terrorism_Analysis_Project/figures_and_statistics/Terrorism_Fatalities_Over_Years_ModelFit.png'

        # Perform the visualization (re-run script logic)
        yearly_data = self.cleaned_data.groupby('iyear')['nkill'].sum().reset_index()

        # Extract year (X) and total fatalities (y)
        X = yearly_data['iyear'].values
        y = yearly_data['nkill'].values

        # Normalize year for numerical stability
        X_normalised = X - 1970

        # Log-transform fatalities for linear regression
        log_y = np.log(y)

        # Perform linear regression
        X_with_intercept = np.c_[np.ones(X_normalised.shape[0]), X_normalised]
        beta = np.linalg.inv(X_with_intercept.T @ X_with_intercept) @ X_with_intercept.T @ log_y

        # Extract parameters
        ln_a = beta[0]
        b = beta[1]
        a = np.exp(ln_a)

        # Generate predictions
        y_pred = a * np.exp(b * X_normalised)

        # Plot and save the visualization
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.scatter(X, y, alpha=0.7, label="Actual Fatalities", color='blue', marker='x')
        plt.plot(X, y_pred, color='orange', linewidth=2,
                 label=f'Exponential Fit: y = {a:.2f} * e^({b:.4f} * (t - 1970))')
        plt.title("Exponential Model Fit: Year vs. Total Fatalities", fontsize=14)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Total Fatalities", fontsize=12)
        plt.ylim(0, None)
        plt.legend()
        plt.grid(True)
        plt.savefig(figure_path, bbox_inches='tight')
        plt.clf()

        # Check if the file exists
        self.assertTrue(os.path.exists(figure_path), f"Visualization file not created at {figure_path}.")

if __name__ == "__main__":
    unittest.main()
