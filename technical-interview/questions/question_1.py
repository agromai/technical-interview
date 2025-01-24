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
import pandas as pd


df = pd.read_csv('technical-interview\data\sales_data.csv')

def handle_na_values(df: pd.DataFrame, col_name: str, mode: bool = False) -> pd.DataFrame:
   if mode:
      df.loc[df[col_name].isna(), col_name] = df[col_name].mode()[0]
   else:
      df.loc[df[col_name].isna(), col_name] = df[col_name].mean()
   return df


def create_summary(df: pd.DataFrame, count_na: pd.Series):
   # Total sales by category
   total_sales = df.groupby('category').size()

   # Average price by category
   avg_price = df.groupby('category')['price'].mean()

   # Combine into a single DataFrame
   summary_df = pd.DataFrame({
        "Total Sales": total_sales,
        "Average Price": avg_price,
        "Missing Price Values Handled": count_na
    }).reset_index()

   return summary_df


if __name__ == '__main__':
   # Convert date string to datetime
   df['sale_date'] = pd.to_datetime(df['sale_date'])

   # CountNA only when data is not handled
   count_na = df.isna().sum()
   # Price NaN values after category handling
   price_na = df.groupby('category')['price'].apply(lambda x: x.isna().sum())

   df = handle_na_values(df, 'category', True)
   # Price NaN values before category handling
   price_na_2 = df.groupby('category')['price'].apply(lambda x: x.isna().sum())
   
   df = handle_na_values(df, 'price')
   summary_df = create_summary(df, price_na_2)
   summary_df.to_csv('summary_sales_data.csv')
   print(f"{count_na['category']} null values on category columns converted to {df['category'].mode()[0]}")
   print(f"{count_na['price']} null values on price columns converted to its mean value")
