"""
Question 2: Customer Purchase Analysis

Using the provided dataset 'customer_purchases.csv', perform the following analyses:

1. Calculate the following metrics per customer:
   - Total amount spent
   - Average purchase value
   - Number of purchases
   - Most frequently bought category
"""
import pandas as pd
import sys

# Redirect print output to a file
output_file = './technical-interview/questions/questions_outputs_logs/output_question_2.txt'
with open(output_file, 'w') as f:
    sys.stdout = f  # Redirect stdout to the file

    # Load the dataset
    df = pd.read_csv("./technical-interview/data/customer_purchases.csv")

    # 1. Metrics per customer
    df_per_customer = df.groupby('customer_id')['amount'].agg(['sum', 'mean', 'count'])
    df_per_customer.columns = ['total_spent', 'average_spent', 'number_of_purchases']

    df_category_max_per_customer = df.groupby('customer_id')['category'].apply(lambda x: x.mode()[0])
    df_per_customer['most_common_category'] = df_category_max_per_customer

    print("\nMatrix of metrics per customer:\n")
    print(df_per_customer.head(10))

    """
    2. Create a summary DataFrame with:
       - Top 5 customers by total spend
       - Bottom 5 customers by total spend
    """
    df_top_5_spent = df_per_customer.sort_values('total_spent', ascending=False).head(5)
    df_bottom_5_spent = df_per_customer.sort_values('total_spent', ascending=False).tail(5)

    print("\nTop 5 customers by total spend:", df_top_5_spent, "\nBottom 5 customers by total spend", df_bottom_5_spent, sep="\n")

    """
    3. Calculate the monthly purchase trends:
       - Total sales per month
       - Average purchase value per month
    """
    df['purchase_date'] = pd.to_datetime(df['purchase_date'], errors='coerce')
    if df['purchase_date'].dtype == 'datetime64[ns]':
        if df['purchase_date'].isnull().sum() == 0:
            print("\nTransformation successful.\n")
        else:
            print("\nInvalid values converted to NaT.\n")
    else:
        print("\nError transforming type.\n")

    df_per_date = df.groupby(df['purchase_date'].dt.to_period('M'))

    print("\nTotal sales per month\n", df_per_date['amount'].sum().round(2).to_string(header=False))
    print("\nAverage purchase value per month\n", df_per_date['amount'].mean().round(2).to_string(header=False))

    """
    Bonus: Identify any customers who haven't made a purchase in the last 3 months
    """
    today_fake = df['purchase_date'].max()
    last_3_months = today_fake - pd.DateOffset(months=3)
    clientes_inativos = df[~df['customer_id'].isin(df[df['purchase_date'] >= last_3_months]['customer_id'])]['customer_id'].unique()
    print("\nList of inactive customers in the last three months:\n", clientes_inativos)

# Restore stdout to default
sys.stdout = sys.__stdout__
print(f"Output written to {output_file}")