# Customer 360° Intelligence & Churn Prevention Platform

## Project Overview

The Customer 360° Intelligence & Churn Prevention Platform is a data analytics project designed to create a unified view of customer behavior and identify customers who may require retention-focused attention.

The project combines customer, order, payment, return, support, marketing and engagement data to analyze customer value, RFM behavior and churn risk.

## Business Problem

Businesses collect customer information across multiple systems. Without a unified customer view, it becomes difficult to identify valuable customers, understand customer behavior and detect customers who may be at higher churn risk.

This project addresses this problem by integrating and analyzing customer-related data through a complete analytics workflow.

## Project Objectives

- Build a unified Customer 360° dataset
- Analyze customer value and purchasing behavior
- Perform RFM analysis
- Identify churn-risk categories
- Analyze customer support and digital engagement
- Create business-focused dashboards
- Generate retention-oriented insights

## Dataset

The final Customer 360° dataset contains:

- 10,000 customers
- 57 analytical features

The dataset includes customer information, transaction behavior, engagement indicators, RFM metrics, churn indicators and retention-related fields.

## Technology Stack

- Python
- Pandas
- NumPy
- MySQL
- MongoDB
- Advanced Excel
- Power BI
- Tableau
- Orange Data Mining

## Project Workflow

Raw Data
↓
Python Data Generation & Validation
↓
MySQL Data Storage
↓
MongoDB Event Workflow
↓
Customer 360° Dataset
↓
RFM & Churn Analysis
↓
Excel Analysis
↓
Power BI Dashboard
↓
Tableau Analysis
↓
Orange Exploratory Analysis
↓
Business Insights & Retention Actions

## Python

Python was used for data generation, validation, transformation and preparation of analytical datasets.

Key Python libraries:

- Pandas
- NumPy

The Python workflow includes customer data generation, business data preparation, validation, MySQL loading, Customer 360° preparation, RFM analysis and churn dataset preparation.

## MySQL

MySQL was used as the relational database layer for structured business data.

The database contains business entities such as:

- Customers
- Products
- Stores
- Orders
- Order Items
- Payments
- Returns
- Support Tickets
- Marketing Campaigns
- Customer Campaigns

SQL was also used for validation and analytical queries.

## MongoDB

MongoDB was used as part of the event-oriented data workflow for customer activity/event data.

Python was used to generate and prepare MongoDB-oriented customer event data.

## Advanced Excel

Advanced Excel was used for exploratory business analysis and summary reporting.

Analysis included:

- Customer value analysis
- Revenue analysis
- RFM analysis
- Churn risk analysis
- Support and engagement analysis
- PivotTables and charts

## Power BI

Power BI was used to build the main interactive business intelligence dashboard.

Dashboard pages include:

1. Executive Overview
2. Churn & Retention
3. Customer 360° Profile

The Power BI report contains 34 visuals across these pages.

## Tableau

Tableau was used for additional customer behavior visualization.

Key analyses include:

- Customers by Churn Risk Category
- Customers by Value Segment
- Customers by RFM Segment
- Average Churn Risk Score by Category
- Customers by Digital Activity
- Customers by Support Ticket Status

## Orange Data Mining

Orange was used for exploratory analysis of the Customer 360° dataset.

The workflow included:

- Data Table
- Distributions
- Box Plot
- Scatter Plot

The analysis explored relationships between customer behavior, revenue, orders and churn-related variables.

## Key Analytical Findings

The Customer 360° analysis identified different levels of customer churn risk.

Churn Risk Category distribution:

- Critical: 3,958
- High: 2,331
- Medium: 3,176
- Low: 525

Total customers analyzed: 10,000.

High + Critical risk customers: 6,289.

These results indicate that a substantial customer group requires further retention-focused analysis and targeted business attention.

## Business Use

The analytical outputs can support:

- Customer retention planning
- High-risk customer identification
- Customer value analysis
- RFM-based segmentation
- Support prioritization
- Campaign targeting
- Customer engagement analysis

## Project Structure

Customer_360_Churn_Platform/

├── 01_Business_Requirements  
├── 02_Raw_Data  
├── 03_Python  
├── 04_MySQL  
├── 05_MongoDB  
├── 06_Excel  
├── 07_PowerBI  
├── 08_Tableau  
├── 09_Orange  
├── 10_Documentation  
└── 11_Final_Presentation

## Main Deliverables

- Python data processing scripts
- MySQL database and SQL analysis
- Customer 360° dataset
- Advanced Excel analysis
- Power BI dashboard
- Tableau analysis
- Orange workflow
- Project documentation
- Final presentation

## Conclusion

This project demonstrates an end-to-end data analytics workflow covering data preparation, database management, customer analytics, visualization and business-focused insight generation.

The final solution provides a structured Customer 360° view that can be used to understand customer behavior, identify churn-risk groups and support retention-focused decision making.