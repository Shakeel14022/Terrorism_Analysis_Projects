import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
from dataset_loader import load_dataset
from dataset_cleaner import clean_dataset

# Load and clean the dataset
raw_data = load_dataset()
if raw_data is not None:
    data = clean_dataset(raw_data)

    # Filter data for ANOVA visualization
    filtered_data = data[['nkill', 'attacktype1_txt']].dropna()

    # Group by attack type to calculate mean and confidence intervals
    grouped = filtered_data.groupby('attacktype1_txt')['nkill'].agg(['mean', 'count', 'std']).reset_index()
    grouped = grouped[grouped['count'] > 1]  # Exclude groups with a single data point

    # Calculate the 95% confidence interval for each attack type
    z_value = stats.norm.ppf(0.975)  # For 95% confidence
    grouped['ci'] = z_value * (grouped['std'] / np.sqrt(grouped['count']))

    # Plotting with adjusted y-axis
    plt.figure(figsize=(10, 6))

    # Bar plot with color palette optimised for color theory
    colors = plt.cm.viridis(np.linspace(0, 1, len(grouped['attacktype1_txt'])))
    plt.bar(grouped['attacktype1_txt'], grouped['mean'], yerr=grouped['ci'], capsize=5, alpha=0.85, color=colors)

    # Adjust y-axis to start at 0 and have an upper bound of 12
    plt.ylim(bottom=0, top=12)
    plt.xticks(rotation=45, ha='right')

    # Add labels, title, and caption
    plt.xlabel('Attack Type', fontsize=12)
    plt.ylabel('Mean Fatalities', fontsize=12)
    plt.title('Mean Fatalities by Attack Type with 95% Confidence Intervals', fontsize=14)
    plt.figtext(0.5, -0.32, 'The mean number of fatalities per terrorist attack type, with 95% Confidence Intervals',
                wrap=True, horizontalalignment='center', fontsize=10)

    # Save the figure in the correct directory
    plt.savefig('Terrorism_Analysis_Project/figures_and_statistics/95_ConfidenceInterval_Fatalities_By_Attacktype.png', bbox_inches='tight')
