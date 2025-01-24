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
#%%
# Required libraries

import pandas as pd

#%%
# Functions
def clean_display(info):
    """

    Parameters
    ----------
    info : str
        The information to be printed.

    Returns
    -------
    None.

    """
    print("#"*79)
    print(info.center(79))
    print("#"*79,"\n")

#%%


file_path = '../data/customer_purchases.csv'
customer_df = pd.read_csv(file_path)
customer_df_bckp = customer_df.copy() # Separate copy of the df if necessary


print(customer_df.info(),"\n")

#%% 

# 1) Calculating metrics

# Use pandas.DataFrameGroupBy.agg to create a dataframe with required metrics
customer_metrics = customer_df.groupby('customer_id').agg(
    Total_Spent=('amount', 'sum'),  # Total amount spent
    Avg_Purchase=('amount', lambda x: round(x.mean(),2)), 
    N_Purchases=('purchase_id', 'count'),  
    Most_Frequent_Category=('category', lambda x: x.mode()[0])  
)
clean_display("METRICS PER CUSTOMER")
print(customer_metrics,"\n")


#%%

# 2) Ranking clients

# Sort by total spend to get the top 5 and bottom 5 customers
top_5_customers = customer_metrics.nlargest(5, 'Total_Spent')
bottom_5_customers = customer_metrics.nsmallest(5, 'Total_Spent')

# Create a summary dataframe for top 5 and bottom 5 customers by total spend
rank_customers = pd.concat([
    top_5_customers.assign(Rank='Top 5'),
    bottom_5_customers.assign(Rank='Bottom 5')
])

clean_display("RANK OF CUSTOMERS")
print(rank_customers,"\n")

#%%

# 3) Monthly purchase trends

# Convert to datetime format 
customer_df['purchase_date'] = pd.to_datetime(customer_df['purchase_date'])

# Calculate the month from the purchase_date
customer_df['month'] = customer_df['purchase_date'].dt.to_period('M')

# Calculate total sales and average purchase value per month
monthly_trends = customer_df.groupby('month').agg(
    total_sales=('amount', 'sum'),
    average_purchase_value=('amount', lambda x: round(x.mean(),2))
)

clean_display("MONTHLY TRENDS")
print(monthly_trends,"\n")

#%%

# Bonus: Customers who haven't made a purchase in the last 3 months

date_last_purchase = customer_df['purchase_date'].max()
three_months = date_last_purchase - pd.DateOffset(months=3)

# Mask to filter customers who made purchases in the last 3 months
recent_customers = customer_df[customer_df['purchase_date'] > 
                               three_months]['customer_id'].unique()

# Use inverse operation of the mask to identify customers 
# who haven't made purchases in the last 3 months
inactive_customers_array = customer_df[~customer_df['customer_id'].isin(
    recent_customers)]['customer_id'].unique()

inactive_customers = pd.DataFrame(
    {'Customer ID': inactive_customers_array})

clean_display("INACTIVE CUSTOMERS ")
print(inactive_customers)

