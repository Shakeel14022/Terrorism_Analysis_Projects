import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from dataset_loader import load_dataset
from dataset_cleaner import clean_dataset

# Load and clean the dataset
raw_data = load_dataset()
if raw_data is not None:
    data = clean_dataset(raw_data)

    # Aggregate fatalities by year
    yearly_data = data.groupby('iyear')['nkill'].sum().reset_index()

    # Extract year (X) and total fatalities (y)
    X = yearly_data['iyear'].values
    y = yearly_data['nkill'].values

    # Normalise year for numerical stability
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

    # Calculate residuals of modelfit
    residuals = y - y_pred

    # Plot the results
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

    plt.figtext(0.5, -0.1, 'Figure 1: An exponential model fit over a scatterplot that explores changes in total fatalities\n' 
            'resulted from terrorist incidents every year, from 1970 to 2020. The model of equation:\n'
            'y = 820.55 * e^(0.0738 * (t - 1970)), suggests an exponential average increasing trend, of approx 7.38% rise in\n' 
            'terrorism related fatalities per year.',
            wrap=True, horizontalalignment='center', fontsize=10)
        
    # Save the figure
    plt.savefig('Terrorism_Analysis_Project/figures_and_statistics/Terrorism_Fatalities_Over_Years_ModelFit.png', bbox_inches='tight')


    # Create a vertical boxplot with labeled axes and a caption
    plt.figure(figsize=(8, 6))
    plt.boxplot(residuals, vert=True, patch_artist=True, boxprops=dict(facecolor="lightblue"))
    plt.title("Boxplot of Residuals", fontsize=14)
    plt.xlabel("Residuals", fontsize=12)
    plt.ylabel("Residual Values", fontsize=12)
    plt.grid(True)
    plt.figtext(0.5, -0.09, 'Sub-Figure 1: This boxplot illustrates the spread and variability of the residuals from the exponential model fit.\n'
            'The y-axis represents the residual values. There appears to be a relatively normal distribution to the residuals of\n'
            'the model, with a relatively symmetrical structure around/close to 0. The 2 positive outlier points highlight the\n'
            'extreme nature of terrorism and terrorist attacks - with some years far exceeding the predictions of the model fit.', 
            wrap=True, horizontalalignment='center', fontsize=10)
    plt.savefig('Terrorism_Analysis_Project/figures_and_statistics/Boxplot_of_Residuals.png', bbox_inches='tight')


    # Exponential model equation as a string
    model_equation = f"Exponential Model Equation: y(t) = {a:.2f} * e^({b:.4f} * (t - 1970))"

    # Path to the statistics.txt file
    statistics_file = 'Terrorism_Analysis_Project/figures_and_statistics/statistics.txt'

    # Print and append the model equation to the statistics file
    with open(statistics_file, 'a') as f:
        f.write("\n--- Exponential Model Equation ---\n")
        f.write(model_equation + "\n")
    
# Calculate correlation
correlation_coefficient, p_value = pearsonr(X_normalised, log_y)

# Prepare the result as a string
correlation_result = (
    "\nCorrelation Analysis: Correlation between transformed variables\n"
    "-----------------------------------------------------\n"
    f"Pearson Correlation Coefficient: {correlation_coefficient:.3f}\n"
    f"P-Value: {p_value:.2e}\n\n"
)

# Append the result to the statistics.txt file
with open(statistics_file, "a") as f:
     f.write(correlation_result)

print("Correlation results added to statistics.txt")
