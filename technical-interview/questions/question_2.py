"""
Question 2: Customer Purchase Analysis

Using the provided dataset 'customer_purchases.csv', perform the following analyses:

1. Calculate the following metrics per customer:
   - Total amount spent
   - Average purchase value
   - Number of purchases
   - Most frequently bought category

2. Create a summary DataFrame with:
   - Top 5 customers by total spend
   - Bottom 5 customers by total spend

3. Calculate the monthly purchase trends:
   - Total sales per month
   - Average purchase value per month

Bonus: Identify any customers who haven't made a purchase in the last 3 months
"""

# Your code here

import pandas as pd 
import os

cwd = os.getcwd()

# Load Dataset
dataset_path = os.path.join(cwd, "technical-interview/data/customer_purchases.csv")
customer_dataset = pd.read_csv(dataset_path)

# Total amount spent
total_amount = customer_dataset.groupby('customer_id')['amount'].sum()
print("\n------ Total amount spent per customer: ------\n")
print(total_amount.to_string())

# Average purchase value:
average_purchase = customer_dataset.groupby('customer_id')['amount'].mean()
print("\n------ Average purchase value per customer: ------\n")
print(average_purchase.to_string())

# Number of purchases
total_purchases = customer_dataset.groupby('customer_id',)['amount'].count()
print("\n------ Number of purchases per customer: ------\n")
print(total_purchases.to_string())

print("\n------Top 5 customers by total spend: ------\n")
top5_spend = total_amount.sort_values(ascending=False)[0:5]
print(top5_spend.to_string())

print("\n------ Bottom 5 customers by total spend: ------\n")
bottom5_spend = total_amount.sort_values()[0:5]
print(bottom5_spend.to_string())

# Add column month to visualize
dataset_month = customer_dataset
dataset_month['Month'] = dataset_month['purchase_date'].str[5:7]

# Total amount spent
sales_month = dataset_month.groupby("Month")['amount'].sum()
print("\n------ Total sales per month: ------\n")
print(sales_month.to_string())

# Average purchase value per month
average_month = dataset_month.groupby("Month")['amount'].mean()
print("\n------Average purchase value per month: ------\n")
print(average_month.to_string())
