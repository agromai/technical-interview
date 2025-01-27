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


class Q1:
    def __init__(self, data_file="../data/sales_data.csv"):
        self._data = pd.read_csv(data_file)
        self._summary_data = {}
        self._summary_data["missing"] = int(self._data.isna().sum().sum())
        self._clear_data()
        self._summary()

    def _clear_data(self):
        mean_price = self._data.groupby('category')['price'].transform('mean')
        self._data["price"] = self._data["price"].fillna(mean_price)
        mode_category = self._data["category"].mode()[0]
        self._data["category"] = self._data["category"].fillna(mode_category)
        self._data["sale_date"] = pd.to_datetime(self._data["sale_date"])

    def _summary(self):
        self._summary_data["sales"] = (
            self._data.groupby("category")["quantity"].sum().reset_index()
        )
        self._summary_data["average"] = (
            self._data.groupby("category")["price"].mean().reset_index()
        )

    def get_summary(self):
        return self._summary_data

    def get_data(self):
        return self._data
