from scipy import stats
import pandas as pd
from pingouin import welch_anova
from dataset_loader import load_dataset
from dataset_cleaner import clean_dataset

# Load and clean the dataset
raw_data = load_dataset()
if raw_data is not None:
    data = clean_dataset(raw_data)

    # Perform Welch's ANOVA
    filtered_data = data[['nkill', 'attacktype1_txt']].dropna()
    welch_results = welch_anova(data=filtered_data, dv='nkill', between='attacktype1_txt')

    # Calculate descriptive statistics
    desc_stats = filtered_data.groupby('attacktype1_txt')['nkill'].agg(['count', 'mean', 'std']).round(2)

    # Path to the statistics.txt file
    statistics_file = 'Terrorism_Analysis_Project/figures_and_statistics/statistics.txt'


    # Append results to statistics.txt
    with open(statistics_file, 'a') as f:
        f.write("\n--- Descriptive Statistics of fatalities by Attack Type ---\n")
        f.write(desc_stats.to_string(index=True))  # Write descriptive statistics as a string
        f.write("\n\n--- Welch ANOVA Results ---\n")
        f.write(welch_results.to_string(index=False))  # Write Welch ANOVA results as a string
        f.write("\n")  # Add a newline for better readability
