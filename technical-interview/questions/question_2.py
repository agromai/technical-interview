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

def calculate_per_customer(df: pd.DataFrame) -> pd.DataFrame:
   total_amount_value = df.groupby('customer_id')['amount'].sum()
   average_value = df.groupby('customer_id')['amount'].mean()
   total_purchases = df.groupby('customer_id').size()
   frequent_category = df.groupby('customer_id')['category'].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
   customer_df = pd.DataFrame({
      "total_spent": total_amount_value,
      "avg_value_spent": average_value,
      "total_purchases": total_purchases,
      "most_frequent_category": frequent_category
   }).reset_index()
   return customer_df

def top_bottom_customers(df: pd.DataFrame, total_spend_col: str = 'total_spent') -> pd.DataFrame:
   customer_df = calculate_per_customer(df)

   top = customer_df.nlargest(5, total_spend_col)
   bottom = customer_df.nsmallest(5, total_spend_col)

   top['classification'] = (
      top[total_spend_col]
      .rank(ascending=False)
      .astype(int)
      .astype(str) + 'º top customer'
   )

   bottom['classification'] = (
      bottom[total_spend_col]
      .rank(ascending=True)
      .astype(int)
      .astype(str) + 'º bottom customer'
   )
   return pd.concat([top, bottom], ignore_index=True)


def calc_month_trend(df: pd.DataFrame) -> pd.DataFrame:
    monthly_trends = df.groupby(pd.Grouper(key='purchase_date', freq='M')).agg(
        total_sales=('amount', 'sum'),
        avg_purchase_value=('amount', 'mean'),
        total_purchases=('purchase_id', 'count')
    ).reset_index()
    return monthly_trends


def calc_customer_month_trend(df: pd.DataFrame) -> pd.DataFrame:
    df['year_month'] = df['purchase_date'].dt.to_period('M')
    
    customer_monthly_trends = df.groupby(['customer_id', 'year_month']).agg(
        total_sales=('amount', 'sum'),
        avg_purchase_value=('amount', 'mean'),
        total_purchases=('purchase_id', 'count')
    ).reset_index()
    customer_monthly_trends['year_month'] = customer_monthly_trends['year_month'].dt.to_timestamp()

    return customer_monthly_trends

def customers_inactive_last_3_months(df: pd.DataFrame) -> pd.DataFrame:
    max_date = df['purchase_date'].max()
    three_months_ago = max_date - pd.DateOffset(months=3)
    
    latest_purchase = df.groupby('customer_id')['purchase_date'].max().reset_index()
    latest_purchase.rename(columns={'purchase_date': 'last_purchase_date'}, inplace=True)
    
    inactive_customers = latest_purchase[latest_purchase['last_purchase_date'] < three_months_ago]
    
    return inactive_customers

if __name__ == '__main__':
   df = pd.read_csv('technical-interview\data\customer_purchases.csv')
   df['purchase_date'] = pd.to_datetime(df['purchase_date'])

   customer_df = calculate_per_customer(df)
   top_bottom_df = top_bottom_customers(df)
   general_month_trends = calc_month_trend(df)
   customer_month_trend = calc_customer_month_trend(df)
   inactive_customers = customers_inactive_last_3_months(df)