# Data Quality Auditor

## Project Objective

Data Quality Auditor is an interactive Streamlit application that automatically checks uploaded CSV and Excel datasets for common data quality issues.

The application provides a data quality score, identifies errors and inconsistencies, and provides recommendations to improve the dataset before further analysis.

## Technologies Used

* Python
* Pandas
* NumPy
* Streamlit
* Plotly
* OpenPyXL

## Data Quality Checks

The application checks for:

* Missing values
* Duplicate records
* Invalid email addresses
* Negative sales values
* Invalid status values
* Inconsistent text values
* Invalid date values
* Numerical outliers

## Key Features

* Upload CSV and Excel files
* Automatically audit uploaded datasets
* Calculate an overall Data Quality Score
* Display missing values by column
* Identify duplicate records
* Detect invalid and inconsistent data
* Identify potential outliers
* Display issue severity levels
* Provide data cleaning recommendations
* Visualize data quality issues
* Preview the uploaded dataset
* Download an audit report

## Project Workflow

Upload Dataset
↓
Data Validation
↓
Quality Checks
↓
Issue Detection
↓
Data Quality Score
↓
Recommendations
↓
Download Audit Report

## Project Structure

```text
Data_Quality_Auditor/
│
├── app.py
├── sample_data.csv
├── sample_data.xlsx
├── requirements.txt
└── README.md
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone <your-github-repository-link>
```

### 2. Navigate to the project folder

```bash
cd Data_Quality_Auditor
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit application

```bash
streamlit run app.py
```

The application will open in your web browser.

## Example Data Quality Issues

The sample dataset contains intentionally introduced issues such as:

* Missing customer information
* Invalid email addresses
* Inconsistent city names
* Negative sales values
* Invalid status values
* Duplicate-like records

These issues allow the application to demonstrate how automated data quality auditing works.

## Skills Demonstrated

* Data Cleaning
* Data Validation
* Data Quality Analysis
* Python
* Pandas
* Streamlit
* Data Visualization
* Error Detection
* Business Data Analysis
* Report Generation

## Future Improvements

* Automated data correction
* Advanced duplicate detection
* Custom validation rules
* PDF report generation
* Database integration
* Advanced data quality scoring
* Additional visualization options

## Project Type

Interactive Data Quality Assessment and Data Cleaning application built using Python and Streamlit.
