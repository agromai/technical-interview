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
import datetime

def load_data():
   path = '../data/sales_data.csv' 
   try:
      # carregar o dataset
      df = pd.read_csv(path)
      
      return df
   
   except FileNotFoundError:
      print(f"File path not found.")
      return None
   except Exception as e:
      print(f"Error loading data - {str(e)}")
      return None
   
def create_summary_stats(df):
    if df is None:
        return None
    
    summary_stats = {}
    
    # total de sales por category
    if 'category' in df.columns:
        sales_category = df['category'].value_counts()
        summary_stats['sales_category'] = sales_category
        print("\nTotal Sales per Category:")
        for category, count in sales_category.items():
            print(f"{category}: {count} sales")
    
    # media de preco por category
    if 'category' in df.columns and 'price' in df.columns:
        mean_price_per_category = df.groupby('category')['price'].mean()
        summary_stats['mean_price_per_category'] = mean_price_per_category
        print("\nMean Price per Category:")
        for category, mean_price in mean_price_per_category.items():
            print(f"{category}: R${mean_price:.2f}")
    
    # resumo geral
    if 'price' in df.columns:
      summary_stats['overall_stats'] = {
         'total_records': len(df),
         'total_revenue': df['price'].sum() if 'quantity' not in df.columns else (df['price'] * df['quantity']).sum(),
         'mean_price_overall': df['price'].mean(),
         'sales_category': sales_category
      }
      
      print("\nSummary Stats:")
      print(f"Total records: {summary_stats['overall_stats']['total_records']}")
      print(f"Average price: ${summary_stats['overall_stats']['mean_price_overall']:.2f}")
      print(f"Category highest sale: {summary_stats['sales_category'].idxmax()} ({summary_stats['sales_category'].max()} sales)")
    
    return summary_stats

def clean_data(df):
   if df is None:
      return None, None
   
   # copia limpa
   new_df = df.copy()
   
   # dicionario pra limpeza
   new_summary = {
      'price_missing_handled': 0,
      'category_missing_handled': 0,
      'date_conversion_success': False
   }
   
   print("\nPre-Cleaning Missing Values:")
   print(new_df.isnull().sum())
   
   # 1. price vazio preenchido com mean
   if 'price' in new_df.columns:
      price_missing_count = new_df['price'].isnull().sum() # somatorio
      if price_missing_count > 0:
         price_mean = new_df['price'].mean()
         new_df['price'] = new_df['price'].fillna(price_mean)
         new_summary['price_missing_handled'] = price_missing_count
      else:
         print("No missing values found in 'price' column")
   
   # 2. price vazio preenchido com mode
   if 'category' in new_df.columns:
      category_missing_count = new_df['category'].isnull().sum()
      if category_missing_count > 0:
         category_mode = new_df['category'].mode()[0] if not new_df['category'].mode().empty else 'Unknown'
         new_df['category'] = new_df['category'].fillna(category_mode)
         new_summary['category_missing_handled'] = category_missing_count
      else:
         print("No missing values found in 'category' column")
   
   # 3. 'sale_date' pra datetime
   if 'sale_date' in new_df.columns:
      try:
         new_df['sale_date'] = pd.to_datetime(new_df['sale_date'])
         new_summary['date_conversion_success'] = True
      except Exception as e:
         new_summary['date_conversion_success'] = False
   
   print("\nPost-Cleaning Missing Values:")
   print(new_df.isnull().sum())
   
   return new_df, new_summary


def calculate_total_revenue_by_category(df):
   df['revenue'] = df['price'] * df['quantity']

   total_revenue_by_category = df.groupby('category')['revenue'].sum().sort_values(ascending=False)
   
   print("\nTotal Sales Revenue by Category:")
   for category, revenue in total_revenue_by_category.items():
      print(f"{category}: R${revenue:.2f}")
   
   return total_revenue_by_category


def main():
    df = load_data()
    create_summary_stats(df)

    if df is not None:
        new_df, new_summary = clean_data(df)
        
        if new_df is not None:
            revenue_by_category = calculate_total_revenue_by_category(new_df)
            summary_stats = create_summary_stats(new_df)

            try:
                new_df.to_csv('../output/new_sales_data.csv', index=False)
            except Exception as e:
                print(f"\nError saving new dataset: {str(e)}")

            return new_df, summary_stats, revenue_by_category

    return None, None, None

if __name__ == "__main__":
    new_data, stats, revenue = main()