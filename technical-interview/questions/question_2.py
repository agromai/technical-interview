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
from datetime import timedelta
import calendar

def load_customer_data():
   path = '../data/customer_purchases.csv'
   try:
      df = pd.read_csv(path)
      
      # purchase_date pra datetime
      df['purchase_date'] = pd.to_datetime(df['purchase_date'])
      
      return df
   
   except FileNotFoundError:
      print(f"File path not found.")
      return None
   except Exception as e:
      print(f"Error loading data - {str(e)}")
      return None

def calculate_customer_metrics(df):
   # agrupar por cliente e calcular 
    customer_metrics = df.groupby('customer_id').agg({
        'amount': ['sum', 'mean', 'count'],
        'category': lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown'
    }).round(2)
    
    customer_metrics.columns = ['total_spent', 'avg_purchase_value', 'num_purchases', 'most_frequent_category']
    
    customer_metrics = customer_metrics.reset_index()
    
    # ordenar por ordem descrescente
    customer_metrics = customer_metrics.sort_values('total_spent', ascending=False)
    
    return customer_metrics

def create_customer_summary(customer_metrics):
    # Top 5 customers by total spend
    top_customers = customer_metrics.head(5).copy()
    top_customers['rank'] = range(1, 6)
    
    # Bottom 5 customers by total spend
    bottom_customers = customer_metrics.tail(5).copy()
    bottom_customers['rank'] = range(len(customer_metrics)-4, len(customer_metrics)+1)
    
    print("Top 5 customers by total spend:")
    for idx, row in top_customers.iterrows():
        print(f"{row['rank']}. {row['customer_id']}: R${row['total_spent']:.2f} "
              f"({row['num_purchases']} purchases, avg: R${row['avg_purchase_value']:.2f})")
    
    print("\nBottom 5 customers by total spend:")
    for idx, row in bottom_customers.iterrows():
        print(f"{row['rank']}. {row['customer_id']}: R${row['total_spent']:.2f} "
              f"({row['num_purchases']} purchases, avg: R${row['avg_purchase_value']:.2f})")
    
    return top_customers, bottom_customers


def calculate_monthly_trends(df):
   df['year_month'] = df['purchase_date'].dt.to_period('M')
   
   # metrica por mes
   monthly_trends = df.groupby('year_month').agg({
      'amount': ['sum', 'mean', 'count'],
      'customer_id': 'nunique'
   }).round(2)

   monthly_trends.columns = ['total_sales', 'avg_purchase_value', 'num_purchases', 'unique_customers']
   monthly_trends = monthly_trends.reset_index()

   # formatar mes
   def format_month(period):
      year = period.year
      month = period.month
      month_name = calendar.month_name[month]
      return f"{month_name} {year}"

   monthly_trends['month'] = monthly_trends['year_month'].apply(format_month)
   
   print("\nMonthly purchase trends:")
   for idx, row in monthly_trends.iterrows():
      print(f"\n{row['month']}: \nR${row['total_sales']:.2f} total \nR${row['avg_purchase_value']:.2f} mean \n{row['num_purchases']} purchases \n{row['unique_customers']} customers")
   
   return monthly_trends


def identify_inactive_customers(df):
    months_threshold = 3  # pode mudar caso queira mais meses
    max_date = df['purchase_date'].max()
    cutoff_date = max_date - timedelta(days=months_threshold * 30)
    
    print(f"\nAnalysis date: {max_date.strftime('%Y-%m-%d')}")
    print(f"Cutoff date: {cutoff_date.strftime('%Y-%m-%d')}")
    
    last_purchase = df.groupby('customer_id')['purchase_date'].max().reset_index()
    last_purchase.columns = ['customer_id', 'last_purchase_date']
    
    # identificar clientes inativos
    inactive_customers = last_purchase[last_purchase['last_purchase_date'] < cutoff_date].copy()

    # calcular dias desde a ultima compra e ordenar
    inactive_customers['days_since_last_purchase'] = (max_date - inactive_customers['last_purchase_date']).dt.days
    inactive_customers = inactive_customers.sort_values('days_since_last_purchase', ascending=False)
    
    if len(inactive_customers) > 0:
        for idx, row in inactive_customers.head(10).iterrows():
            print(f"{row['customer_id']}: {row['days_since_last_purchase']} days "
                  f"(last purchase: {row['last_purchase_date'].strftime('%Y-%m-%d')})")
    
    return inactive_customers
 

def main():   
    df = load_customer_data()
    
    if df is not None:
        customer_metrics = calculate_customer_metrics(df)
        
        top_customers, bottom_customers = create_customer_summary(customer_metrics)
        
        monthly_trends = calculate_monthly_trends(df)
        
        inactive_customers = identify_inactive_customers(df)
        
        top_customers.to_csv('../output/top_customers.csv', index=False)
        bottom_customers.to_csv('../output/bottom_customers.csv', index=False)
        
        return {
            'customer_metrics': customer_metrics,
            'top_customers': top_customers,
            'bottom_customers': bottom_customers,
            'monthly_trends': monthly_trends,
            'inactive_customers': inactive_customers
        }
    
    return None

if __name__ == "__main__":
    results = main()