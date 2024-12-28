import pandas as pd
import matplotlib.pyplot as plt
from dataset_loader import load_dataset
from dataset_cleaner import clean_dataset

# Load and clean the dataset
raw_data = load_dataset()
if raw_data is not None:
    data = clean_dataset(raw_data)

    # Calculate the total number of incidents and success rate per region
    region_data = data.groupby('region_txt').agg(
        incidents=('eventid', 'count'),
        success_rate=('success', 'mean')
    ).sort_values(by='incidents', ascending=False)

    # Create a dual-axis plot
    fig, ax1 = plt.subplots(figsize=(14, 7))

    ax1.bar(region_data.index, region_data['incidents'], color='skyblue', alpha=0.7, label='Number of Incidents')
    ax1.set_xlabel('Region')
    ax1.set_ylabel('Number of Incidents', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xticks(range(len(region_data.index)))
    ax1.set_xticklabels(region_data.index, rotation=45, ha='right')

    ax2 = ax1.twinx()
    ax2.plot(region_data.index, region_data['success_rate'], color='red', marker='o', label='Success Rate')
    ax2.set_ylabel('Success Rate (Proportion)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add legends
    ax1.legend(loc='upper left', bbox_to_anchor=(0, 1.1), title='Bar Chart')  # Adjusted position
    ax2.legend(loc='upper right', bbox_to_anchor=(1, 1.1), title='Line Chart')  # Adjusted position

    plt.figtext(
        0.5, -0.23,
        'This chart shows the total number of terrorist incidents (bars) and their success rate (line) across different regions.\n'
        'The success of a terrorist incident is determined if the motive or element of the attack was fulfilled', 
        wrap=True, horizontalalignment='center', fontsize=10
    )


    plt.title('Number of Incidents and Success Rate by Region')
    # Save the figure
    plt.savefig('Terrorism_Analysis_Project/figures_and_statistics/No_Incidents_And_Success_Rate_By_Region.png', bbox_inches='tight')
