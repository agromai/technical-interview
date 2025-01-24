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

Inplace mode will be deprecated in future versions of pandas.
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

def examine_data(df):
    """
    

    Parameters
    ----------
    df : pandas DataFrame
        Dataframe to examine.

    Returns
    -------
    None.

    """
    clean_display("FIRST FIVE ROWS")
    # Display the first five rows of the dataset 
    print(df.head(),"\n"*2)


    clean_display("INFORMATION ABOUT THE DATAFRAME")
    print(df.info(),"\n"*2)


    clean_display("STATISTICAL DESCRIPTION OF THE DATA")
    print(df.describe(),"\n"*2)


    clean_display("MISSING VALUES")
    print(df.isnull().sum())

#%% 

# 1) Examining the dataset

# Load the dataset
file_path = '../data/sales_data.csv'
sales_df = pd.read_csv(file_path)
sales_df_bckp = sales_df.copy() # Separate copy of the df if necessary


examine_data(sales_df)
#%%

# 2) Cleaning the data

# We have 30 and 49 missing values ​​in the "category" and "price" 
# columns respectively. Let's replace them.

# Replace with mean the missing values in the 'price' column 
price_mean = sales_df['price'].mean()
sales_df['price'] = sales_df['price'].fillna(price_mean)


# Replace with mode the missing values in the 'category' column 
category_mode = sales_df['category'].mode()[0]
sales_df['category'] =  sales_df['category'].fillna(category_mode)

# Convert 'sale_date' column to datetime format 
sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])


# Examine the data again to assure everything was done correctly
clean_display("INFORMATION ABOUT THE DATAFRAME")
print(sales_df.info())


#%%

# 3) Summarizing the data

category = sales_df[['category','quantity']].groupby('category').sum()[
    'quantity'].index

sales_per_cat = sales_df[['category','quantity']].groupby(['category']).sum()[
    'quantity'].values

avg_price_category = sales_df[['category','price']].groupby('category').mean()[
    'price'].values

miss_val = sales_df_bckp[sales_df_bckp['price'].isnull()].groupby(
    'category').size()

summary_df = pd.DataFrame({
    'Category': category,
    'Total Sales': sales_per_cat,
    'Average Price': avg_price_category,
    'Missing Values in Price Handled': miss_val.values
})

clean_display("SUMMARY")
print(summary_df)






