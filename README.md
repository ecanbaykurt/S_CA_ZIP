# S_CA_ZIP - LA County Zip Code Analysis Dashboard

A comprehensive Streamlit dashboard for visualizing and analyzing Los Angeles County zip code data, including composite scores, economic metrics, and demographic information.

## Features

- **Interactive Filters**: Filter by score category, city, and composite score range
- **Overview Analysis**: Distribution charts, top/bottom zip codes
- **Score Analysis**: Component scores, correlations, and relationships
- **Economic Metrics**: Income and home value analysis
- **Demographics**: Population, density, transit, and education metrics
- **Data Table**: Searchable and filterable data table with export functionality

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Dashboard Sections

1. **Overview**: High-level statistics and distributions
2. **Score Analysis**: Detailed analysis of composite and component scores
3. **Economic Metrics**: Income and home value visualizations
4. **Demographics**: Population, density, transit, and education metrics
5. **Data Table**: Interactive table with search and export capabilities

## Data

The dashboard reads from `LA_County_Analysis_Final_with_Scores.csv` which should be in the same directory as `app.py`.
