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
# Function that recives a dataframe and a list of column names and returns a dataframe with the mask of the missing values
def missing_values(data, columns):
   missing = pd.DataFrame()
   missing[columns] = data[columns].isnull()
   return missing

def missing_to_mean(data, missing):
   data = data.fillna(data[~missing].mean())
   return data

def missing_to_mode(data, missing):
   data = data.fillna(data[~missing].mode()[0])
   return data

import pandas as pd
import numpy as np
import os
PATH = os.path.abspath(__file__)

# Loading the dat unsin pandas
data = pd.read_csv(PATH.replace('/questions/question_1.py','/data/sales_data.csv'))

# Displaying the first few rows of the dataset and the data types per column
print(">>>>> Dataset top")
print(data[['price', 'category']].head(20))

print("\n>>>>> Dataset data types")
print(data.dtypes)

# Handling missing values
data['sale_date'] = pd.to_datetime(data['sale_date'])

columns_missing_values = ['price', 'category'] 
missing = missing_values(data, columns_missing_values)
#print(data[columns_missing_values][missing.any(axis=1)])
#print(data[columns_missing_values][missing.all(axis=1)])

# Removing missing values for colunmns_missing_values
for column in columns_missing_values:
   if column == 'price':
      data[column] = missing_to_mean(data[column], missing[column])
   elif column == 'category':
      data[column] = missing_to_mode(data[column], missing[column])

# Summary
print("\n>>>>> Summary")
print("Total number of sales per category:\n")
total_sales = data['category'].value_counts().reset_index()
total_sales.columns = ['category', 'total_sales']
print(total_sales)
# total_sales.to_csv(PATH.replace('/questions/question_1.py','/data/sales_per_category.csv'), index=False)
print("---------------------------------------------------------------")
print("Average price per category:\n")
price_category = data.groupby('category')['price'].mean().reset_index()
price_category.columns = ['category', 'average_price']
print(price_category)
# price_category.to_csv(PATH.replace('/questions/question_1.py','/data/average_price_per_category.csv'), index=False)
print("---------------------------------------------------------------")
print("Number of missing values handled:\n")
print("Missing values at")
tot = 0
for column in columns_missing_values:
   tot = tot + missing[column].sum()
   print(f"\t{column}: {missing[column].sum()}")
print("\tTotal: ", tot)
# Save the cleaned dataset
# data.to_csv(PATH.replace('/questions/question_1.py','/data/cleaned_sales_data.csv'), index=False)

# Save all outputs as CSV files
print("\n>>>>> Saving outputs")
print("To save the outputs as CSV files, uncomment the corresponding lines in the code")
