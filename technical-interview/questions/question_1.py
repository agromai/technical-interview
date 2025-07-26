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

# Your code here

import pandas as pd 
from datetime import datetime
import os

cwd = os.getcwd()

# Load Dataset
sales_path = os.path.join(cwd, "technical-interview/data/sales_data.csv")
sales_dataset = pd.read_csv(sales_path)

# Counting NaN Values
price_NaN_values = sales_dataset['price'].isna().sum()
category_NaN_values = sales_dataset['category'].isna().sum()

# Replace NaN values in 'price' with mean
sales_dataset['price'] = sales_dataset['price'].fillna(sales_dataset['price'].mean())

# Replace NaN values in 'category' with most frequently occuring category 
sales_dataset = sales_dataset.fillna(sales_dataset['category'].mode().iloc[0])

# Convert to datetime
sales_dataset['sale_date'] = pd.to_datetime(sales_dataset['sale_date'])

# Summary

sales_count = sales_dataset.groupby("category")['quantity'].count()
price_average = sales_dataset.groupby("category")['price'].mean()

print(" -------- SUMMARY -------- ")

print("\nNumber of sales per category:")
print(sales_count.to_string())

print("\nAverage price per category:")
print(price_average.to_string())

print("\nPrice missing values: ", format(price_NaN_values))
print("\nCategory missing values: ", format(category_NaN_values))

# Save cleanned dataset
sales_dataset.to_csv("technical-interview/data/cleaned_sales_data.csv", index=False)