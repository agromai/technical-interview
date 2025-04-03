"""
Question 1: Data Cleaning and Basic Analysis

Using the provided dataset 'sales_data.csv', perform the following tasks:
1. Load and examine the dataset
"""

import pandas as pd
import sys

# Redirect print output to a file
output_file = './technical-interview/questions/questions_outputs_logs/output_question_1.txt'
with open(output_file, 'w') as f:
    sys.stdout = f  # Redirect stdout to the file

    # Load the dataset
    df = pd.read_csv("./technical-interview/data/sales_data.csv")

    """
    # 2. Clean the data:
       - Handle missing values in the 'price' column (replace with mean)
       - Handle missing values in the 'category' column (replace with mode)
       - Convert 'sale_date' to datetime

    The strategy for replacing price values:
    - Calculate the mean of price without null values.
    - Replace null values with this mean.
    - Note: null values represent only 5% of the total values.
       - The difference between the means appears at the 14th decimal place.
       - Therefore, considering the context of the data, it would not be necessary to do this.
    """

    price_mean_notnull = df[df['price'].isnull() == False]['price'].mean()
    df.fillna({'price': price_mean_notnull}, inplace=True)

    if (df['price'].isnull().sum() == 0):
        print("Price replacement successful!\n")
    else:
        print("Error replacing price.")

    category_mode = df['category'].mode()[0]
    df.fillna({'category': category_mode}, inplace=True)

    if (df['category'].isnull().sum() == 0):
        print("Category replacement successful!\n")
    else:
        print("Error replacing category.")

    df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
    if df['sale_date'].dtype == 'datetime64[ns]':
        if df['sale_date'].isnull().sum() == 0:
            print("Sale date type transformation successful.\n")
        else:
            print("Invalid values converted to NaT.")
    else:
        print("Error transforming sale date type.")

    """
    3. Create a summary of:
       - Total number of sales per category
       - Average price per category
       - Number of missing values handled

    The cleaned dataset should be ready for further analysis.
    """
    print("Total number of sales per category:", df['category'].value_counts().to_string(header=False), sep='\n')

    print("\nAverage price per category:", df.groupby('category')['price'].mean().round(2).to_string(header=False), sep='\n')

    print("\nNumber of missing values:", df.isnull().sum().to_string(header=False), sep='\n')

    df.to_csv('./technical-interview/data/sales_data_clean1.csv', index=False)

# Restore stdout to default
sys.stdout = sys.__stdout__
print(f"Output written to {output_file}")