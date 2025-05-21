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
import os

path_csv = os.path.join(os.getcwd(),'..','data','sales_data.csv')
file = pd.read_csv(path_csv)

print(file.info())

# Data cleaning 
file['price'] = file['price'].fillna(file['price'].mean())

file['category'] = file['category'].fillna(file['category'].mode()[0])

file['sale_date'] = pd.to_datetime(file['sale_date'], errors='coerce')

# Counts the total number of sales for each category
total_sales_category = file['category'].value_counts()
print("\nTotal number of sales per category: ")
print(total_sales_category)

# Calculates the average price for each category.
average_price_category = file.groupby('category')['price'].mean()
print("\nAverage price per category: ")
print(average_price_category)

print("\nNumber of missing values handled: ")
print("\nPrice: ")
missing_price_values = file['price'].isnull().sum()
print(missing_price_values)
print("\nCategory: ")
missing_category_values = file['category'].isnull().sum()
print(missing_category_values)