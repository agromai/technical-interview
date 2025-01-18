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

from datetime import datetime, timedelta

df2 = pd.read_csv('customer_purchases.csv')

df2.info()

df2.describe()

df2['purchase_date'] = pd.to_datetime(df2['purchase_date'])

##### 1.
# Total amount spent
total_spent = df2.groupby('customer_id')['amount'].sum().reset_index()
total_spent.rename(columns={'amount': 'total_spent'}, inplace=True)

# Average purchase value
avg_purchase_value = df2.groupby('customer_id')['amount'].mean().reset_index()
avg_purchase_value.rename(columns={'amount': 'avg_purchase_value'}, inplace=True)

# Number of purchases
num_purchases = df2.groupby('customer_id')['purchase_id'].count().reset_index()
num_purchases.rename(columns={'purchase_id': 'num_purchases'}, inplace=True)

# Most frequently bought category
most_frequent_category = df2.groupby('customer_id')['category'].agg(lambda x: x.mode()[0]).reset_index()
most_frequent_category.rename(columns={'category': 'most_frequent_category'}, inplace=True)

customer_metrics = total_spent.merge(avg_purchase_value, on='customer_id')
customer_metrics = customer_metrics.merge(num_purchases, on='customer_id')
customer_metrics = customer_metrics.merge(most_frequent_category, on='customer_id')

print("Customer Metrics:")
print(customer_metrics)

##### 2.
# Sort by total_spent
top_customers = customer_metrics.nlargest(5, 'total_spent')
bottom_customers = customer_metrics.nsmallest(5, 'total_spent')

summary_df = pd.concat([top_customers, bottom_customers], keys=['Top 5', 'Bottom 5'])

print("Top and Bottom Customers by Total Spend:")
print(summary_df)

##### 3.
# Extract month and year
df2['month_year'] = df2['purchase_date'].dt.to_period('M')

# Group by month_year and calculate total sales
total_sales = df2.groupby('month_year')['amount'].sum().reset_index()
total_sales.rename(columns={'amount': 'total_sales'}, inplace=True)

# Group by month_year and calculate average purchase value
avg_purchase_value = df2.groupby('month_year')['amount'].mean().reset_index()
avg_purchase_value.rename(columns={'amount': 'avg_purchase_value'}, inplace=True)

# Combine metrics into a single DataFrame
monthly_trends = total_sales.merge(avg_purchase_value, on='month_year')

print("Monthly Trends (Combined):")
print(monthly_trends.head())


##### BONUS
# Calculate the last purchase date for each customer
last_purchase_date = df2.groupby('customer_id')['purchase_date'].max()

# Define the cutoff for the last 3 months
cutoff_date = df2['purchase_date'].max() - timedelta(days=90)

# Filter customers who haven't purchased in the last 3 months
inactive_customers = last_purchase_date[last_purchase_date < cutoff_date].reset_index()
inactive_customers.columns = ['customer_id', 'last_purchase_date']

print("Inactive Customers in the Last 3 Months:")
print(inactive_customers)
