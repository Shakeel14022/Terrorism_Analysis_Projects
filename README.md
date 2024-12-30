# Terrorism Analysis Projects

## Overview

This repository contains the code and analyses for the project **"Understanding Terrorism Dynamics: Patterns, Rising Severity, and Strategic Responses."** The aim of this research is to explore global terrorism trends, focusing on attack types, regional distributions, and fatality rates. The study seeks to provide actionable insights for mitigating terrorism's impact, through the use of visualisations and statistical analysis.

### Research Hypothesis

The project is guided by the hypothesis:
> *"Distinct patterns in terrorist attack types and regional occurrences significantly influence fatality and success rates of terrorist incidents, with a rising severity of attacks highlighting the necessity for targeted prevention measures and policies to mitigate the impact of terrorism globally."*

---

## Project Structure

The repository is structured as follows:

- **`.circleci/`**: Configuration files for CircleCI integration for testing every commit.
  - `config.yml`: CircleCI configuration file.

- **`Terrorism_Analysis_Project/`**
  - **`dataset/`**: Contains the dataset used for analysis.
    - `globalterrorismdatabase_1970_2020_F.csv`: Dataset containing detailed information on global terrorism incidents.

  - **`figures_and_statistics/`**: Stores all visualisations and statistical summaries related to the analysis.
    - `95_ConfidenceInterval_Fatalities_By_Attacktype.png`
    - `Attacktype_Frequency_And_Success.png`
    - `Boxplot_of_Residuals.png`
    - `No_Incidents_And_Success_Rate_By_Region.png`
    - `Terrorism_Fatalities_Over_Years_ModelFit.png`
    - `statistics.txt`: Summary of key statistical findings.

  - **`scripts/`**: Contains all scripts for cleaning data, performing analysis, and generating visualisations.
    - `95_ConfidenceInterval_Fatalities_By_Attacktype.py`
    - `Attacktype_Frequency_And_Success.py`
    - `No_Incidents_And_Success_Rate_By_Region.py`
    - `Terrorism_Fatalities_Over_Years_ModelFit.py`
    - `Welchs_ANOVA_Test.py`
    - `dataset_cleaner.py`: Script to clean the dataset.
    - `dataset_loader.py`: Script to load the cleaned dataset into the analysis pipeline.
    - `requirements.txt`: Lists Python dependencies needed to run the scripts.

  - **`Tests/`**: Includes all test files to validate scripts and functionality.
    - `Test_Suite_Details.txt`: Overview of all tests conducted.
    - `test_Attacktype_Frequency_And_Success_visual.py`
    - `test_ModelFit_visual.py`
    - `test_No_Incidents_And_Success_Rate_By_Region_visual.py`
    - `test_Welchs_ANOVA_Test.py`
    - `test_confidenceinterval_visual.py`
    - `test_dataset_cleaner.py`
    - `test_dataset_loader.py`

- **`README.md`**: Project documentation.

---

## Dataset Information

The analysis is based on data from the **Global Terrorism Database (GTD)**, a comprehensive source documenting over 200,000 international and domestic terrorist attacks from 1970 to 2020. The dataset includes information on attack types, regions, fatalities, and success rates.

### Source: 
The dataset is maintained by the National Consortium for the Study of Terrorism and Responses to Terrorism (START). For more information, visit [GTD’s official page](https://www.start.umd.edu/research-projects/global-terrorism-database-gtd).

---

## Cloning and Running the Repository

To clone and run the project locally, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/Shakeel14022/Terrorism_Analysis_Projects.git
cd Terrorism_Analysis_Projects
```

### 2. Install Required Libraries
Ensure you have Python installed (version 3.8+ is recommended). Install the required dependencies by running:
```bash
pip install -r Terrorism_Analysis_Project/scripts/requirements.txt
```

### 3. Run the Scripts
- **Data Cleaning and Loading**:  
  Use `dataset_cleaner.py` and `dataset_loader.py` to preprocess and load the dataset. Example:
  ```bash
  python Terrorism_Analysis_Project/scripts/dataset_cleaner.py
  python Terrorism_Analysis_Project/scripts/dataset_loader.py
  ```

- **Visualisations and Analysis**:  
  Execute the visualisation and statistical scripts in the `scripts/` directory. Example:
  ```bash
  python Terrorism_Analysis_Project/scripts/Attacktype_Frequency_And_Success.py
  ```

- **Tests**:  
  Run unit tests located in the `Tests/` directory to ensure functionality:
  ```bash
  python -m unittest discover Terrorism_Analysis_Project/Tests
  ```

---

## Creator
This project was conducted by Shakeel Muhammad Rahman
Student ID: 230328914
