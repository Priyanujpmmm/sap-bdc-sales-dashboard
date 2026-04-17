# Sales Analytics Dashboard using SAP Business Data Cloud Architecture (Simulated)

## Overview
This project is an interactive sales analytics dashboard built using Python, Streamlit, Pandas, and Plotly. It simulates the architecture and workflow of SAP Business Data Cloud by demonstrating data ingestion, transformation, analysis, and visualization.

## Problem Statement
Organizations often face difficulty in analyzing sales performance due to scattered records, delayed reporting, and lack of centralized insight generation. This project solves that by providing a dashboard for monitoring sales trends, category performance, regional contribution, customer behavior, and product demand.

## Features
- KPI cards for Total Sales, Total Orders, Total Customers, Average Order Value, and Average Shipping Days
- Monthly sales trend analysis
- Sales by region
- Sales by category
- Sales by segment
- Top 10 states by sales
- Top 10 customers by sales
- Top 10 products by sales
- Download filtered dataset as CSV

## Tech Stack
- Python
- Streamlit
- Pandas
- NumPy
- Plotly

## SAP Business Data Cloud Mapping
- CSV dataset -> Data Source
- Python/Pandas -> Data Processing and Transformation
- Structured analytical model -> Datasphere-like layer
- Streamlit + Plotly dashboard -> SAP Analytics Cloud-like visualization

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py