"""
Question 1: Data Cleaning and Basic Analysis

Using the provided dataset 'sales_data.csv', perform the following tasks:

1. Load and examine the dataset
2. Clean the data:
   - Handle missing values in the 'price' column (replace with mean)
   - Handle missing values in the 'category' column (replace with mode)
   - Convert 'sale_date' to datetime
3. Create a summary of:
   - Total number of sales per category
   - Average price per category
   - Number of missing values handled

The cleaned dataset should be ready for further analysis.
"""

import pandas as pd
import numpy as np

df1 = pd.read_csv('sales_data.csv')  # Load the dataframe
df1.info()  # Get information about the feature types
df1.describe()  # Describe basic statistics for continuous variables

# 2. Clean the data
mean_price = df1['price'].mean()  # Get the mean value of the 'price' column
df1['price'].fillna(mean_price, inplace=True)  # Impute mean for NA values in 'price'

mode_category = df1['category'].mode()[0]  # Get the mode value of 'category'
df1['category'].fillna(mode_category, inplace=True)  # Impute mode for NA values in 'category'

# 3. Create a summary
df1['sale_date'] = pd.to_datetime(df1['sale_date'])  # Convert 'sale_date' to datetime

total_sales_per_category = df1.groupby('category').size()  # Total number of sales per category

average_price_per_category = df1.groupby('category')['price'].mean()  # Average price per category

missing_values_handled = df1.isnull().sum()  # Number of missing values handled

# Output results
print("\nCleaned DataFrame:")
print(df1.head())

print("\nSummary:")
print("Total number of sales per category:")
print(total_sales_per_category)

print("\nAverage price per category:")
print(average_price_per_category)

print("\nNumber of missing values handled:")
print(missing_values_handled)
