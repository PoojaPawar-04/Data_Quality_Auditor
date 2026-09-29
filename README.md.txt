# Data Quality Auditor

An automated data quality auditing web application built using Python, Pandas, and Streamlit.

The application allows users to upload CSV or Excel datasets and automatically identifies common data-quality issues. It provides a data quality score, issue severity analysis, cleaning recommendations, and a downloadable audit report.

---

## Project Objective

The objective of this project is to simplify the process of identifying data-quality problems before performing data analysis or building dashboards.

Poor-quality data can lead to inaccurate analysis and incorrect business decisions. This tool helps users quickly audit their datasets and understand the issues that need attention.

---

## Technologies Used

- Python
- Pandas
- Regular Expressions
- Streamlit
- Excel / CSV
- GitHub

---

## Data Quality Checks

The application checks for:

- Missing values
- Duplicate records
- Invalid email addresses
- Negative sales values
- Invalid status values
- Inconsistent text values
- Invalid dates
- Numerical outliers using the IQR method

---

## Key Features

### Dataset Overview

Displays:

- Total rows
- Total columns
- Missing values
- Duplicate rows

### Data Quality Audit

Identifies data-quality issues and classifies them by severity:

- High
- Medium
- Low

### Data Quality Score

Calculates an overall percentage-based data quality score.

### Issue Analysis

Provides visual summaries of detected issues and their severity.

### Cleaning Recommendations

Provides suggestions for resolving detected data-quality problems.

### Column Quality Report

Displays:

- Data type
- Missing values
- Unique values
- Completeness percentage

### Audit Report

Users can download the detected issues as a CSV audit report.

---

## Project Structure

Data_Quality_Auditor/

- app.py
- sample_data.csv
- sample_data.xlsx
- README.md
- requirements.txt

---

## How to Run the Project

### 1. Install the required libraries

```bash
pip install -r requirements.txt
