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
import os

path_csv = os.path.join(os.getcwd(),'..','data','customer_purchases.csv')
file = pd.read_csv(path_csv)

# Calculates the total amount spent by each customer
total_amount_spent = file.groupby('customer_id')['amount'].sum()

# Calculates the average purchase value for each customer
average_purchase_value = file.groupby('customer_id')['amount'].mean()

# Counts the number of purchases made by each customer
number_purchases = file.groupby('customer_id')['amount'].count()

# Returns the most frequent value in the given series.
def frequent_category(series):
    return series.mode().iloc[0]

most_frequent_category = file.groupby('customer_id')['category'].agg(frequent_category)

customer_summary = pd.DataFrame({
    'total_amount_spent': total_amount_spent,
    'average_purchase_value': average_purchase_value,
    'number_purchases': number_purchases,
    'most_frequent_category': most_frequent_category
})

top_5_customers = customer_summary.nlargest(5, 'total_amount_spent')
bottom_5_customers = customer_summary.nsmallest(5, 'total_amount_spent')

print("Top 5 customers by total spend:")
print(top_5_customers)
print("\nBottom 5 customers by total spend:")
print(bottom_5_customers)

# Converts the date column to datetime and extracts year and month
file['purchase_date'] = pd.to_datetime(file['purchase_date'])
file['year_month'] = file['purchase_date'].dt.to_period('M')
total_sales_month = file.groupby('year_month')['amount'].sum()
average_purchase_month = file.groupby('year_month')['amount'].mean()

print("\nTotal sales per month:")
print(total_sales_month)
print("\nAverage purchase value per month:")
print(average_purchase_month)