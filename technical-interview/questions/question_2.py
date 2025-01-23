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

import pandas as pd
import numpy as np
import os
PATH = os.path.abspath(__file__)

# Loading the dat unsing pandas

data = pd.read_csv(PATH.replace('/questions/question_2.py','/data/customer_purchases.csv'))

# Displaying the first few rows of the dataset and the data types per column
print(">>>>> Dataset top")
print(data.head(20))

print("\n>>>>> Dataset data types")
print(data.dtypes)

# Handling missing values
data['purchase_date'] = pd.to_datetime(data['purchase_date'])

# Per customer metrics
print(">>>>> Per customer metrics")

print("Total amount spent per customer:\n")
total_amount_spent = data.groupby('customer_id')['amount'].sum().reset_index()
total_amount_spent.columns = ['customer_id', 'total_amount_spent']
print(total_amount_spent)
# total_amount_spent.to_csv(PATH.replace('/questions/question_2.py','/data/amount_spent_per_customer.csv'), index=False)
print("--------------------------------------------")

print("Average purchase value per customer:\n")
average_purchase_value = data.groupby('customer_id')['amount'].mean().reset_index()
average_purchase_value.columns = ['customer_id', 'average_purchase_value']
print(average_purchase_value)
# average_purchase_value.to_csv(PATH.replace('/questions/question_2.py','/data/average_purchase_value_per_customer.csv'), index=False)
print("--------------------------------------------")

print("Number of purchases per customer:\n")
number_of_purchases = data.groupby('customer_id')['purchase_id'].count().reset_index()
number_of_purchases.columns = ['customer_id', 'number_of_purchases']
print(number_of_purchases)
# number_of_purchases.to_csv(PATH.replace('/questions/question_2.py','/data/purchases_per_customer.csv'), index=False)
print("--------------------------------------------")

print("Most frequently bought category per customer:\n")
most_frequently_bought_category = data.groupby('customer_id')['category'].agg(lambda x: x.value_counts().index[0]).reset_index()
most_frequently_bought_category.columns = ['customer_id', 'most_bought_category']
print(most_frequently_bought_category)
# most_frequently_bought_category.to_csv(PATH.replace('/questions/question_2.py','/data/most_bought_category_per_customer.csv'), index=False)

# Summary
print("\n>>>>> Summary")
print("Top 5 customers by total spend:\n")
top_5_customers = total_amount_spent.nlargest(5, 'total_amount_spent').sort_values('total_amount_spent', ascending=False)
print(top_5_customers)
# top_5_customers.to_csv(PATH.replace('/questions/question_2.py','/data/top_5_customers.csv'), index=False)
print("---------------------------------------------------------------")
bottom_5_customers = total_amount_spent.nsmallest(5, 'total_amount_spent').sort_values('total_amount_spent', ascending=True)
print("Bottom 5 customers by total spend:\n")
# bottom_5_customers.to_csv(PATH.replace('/questions/question_2.py','/data/bottom_5_customers.csv'), index=False)
print(bottom_5_customers)

# Monthly purchase trends
print("\n>>>>> Monthly purchase trends")
print("Total sales per month:\n")
total_sales_per_month = data.groupby(data['purchase_date'].dt.to_period("M"))['amount'].sum().reset_index()
total_sales_per_month.columns = ['month', 'total_sales']
print(total_sales_per_month)
# total_sales_per_month.to_csv(PATH.replace('/questions/question_2.py','/data/total_sales_per_month.csv'), index=False)
print("---------------------------------------------------------------")
print("Average purchase value per month:\n")
average_purchase_value_per_month = data.groupby(data['purchase_date'].dt.to_period("M"))['amount'].mean().reset_index()
average_purchase_value_per_month.columns = ['month', 'average_purchase']
print(average_purchase_value_per_month)
# average_purchase_value_per_month.to_csv(PATH.replace('/questions/question_2.py','/data/average_purchase_value_per_month.csv'), index=False)

# Bonus
print("\n>>>>> Bonus")
print("Customers who haven't made a purchase in the last 3 months:\n")
last_purchase_date = data['purchase_date'].max()
three_months_ago = last_purchase_date - pd.DateOffset(months=3)
customers_last_purchase = data.groupby('customer_id')['purchase_date'].max().reset_index()
customers_last_purchase.columns = ['customer_id', 'last_purchase_date']
customers_last_purchase = customers_last_purchase[customers_last_purchase['last_purchase_date'] < three_months_ago]
print(customers_last_purchase)
# customers_last_purchase.to_csv(PATH.replace('/questions/question_2.py','/data/Bonus.csv'), index=False)

# Save all outputs as CSV files
print("\n>>>>> Saving outputs")
print("To save the outputs as CSV files, uncomment the corresponding lines in the code")