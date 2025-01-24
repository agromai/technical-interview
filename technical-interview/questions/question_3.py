"""
Question 3: Sales Visualization

Using the cleaned dataset from Question 1 ('sales_data.csv'), create the following visualizations:

1. Create a line plot showing daily sales trends over time
   - Include a 7-day moving average line

2. Create a bar plot showing:
   - Total sales by category
   - Include error bars representing standard deviation

3. Create a scatter plot showing:
   - Relationship between quantity and price
   - Color points by category
   - Add a trend line

Requirements:
- Use appropriate labels and titles
- Include a legend where necessary
- Use a consistent color scheme
- Save all plots as PNG files
"""

#%%
# Required libraries

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
#%% 

# OBS.: I decided to use the same file and clean the dataset again to avoid
# exporting the cleaned dataset to another CSV and creating an additional 
# file.

# Load the dataset
file_path = '../data/sales_data.csv'
sales_df = pd.read_csv(file_path)
sales_df_bckp = sales_df.copy() # Separate copy of the df if necessary

#%%

# Cleaning the data

# Replace with mean the missing values in the 'price' column 
price_mean = sales_df['price'].mean()
sales_df['price'] = sales_df['price'].fillna(price_mean)


# Replace with mode the missing values in the 'category' column 
category_mode = sales_df['category'].mode()[0]
sales_df['category'] =  sales_df['category'].fillna(category_mode)

# Convert 'sale_date' column to datetime format 
sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])

print(sales_df.info())
#%%

# 1) Line plot showing daily sales trends over time

# Calculate daily sales by multiplying 'price' * 'quantity'
sales_df['total_sales'] = sales_df['price'] * sales_df['quantity']
daily_sales = sales_df.groupby('sale_date')['total_sales'].sum().reset_index()

# Add a 7-day moving average column
daily_sales['7_day_moving_avg'] = daily_sales['total_sales'].rolling(
    window=7).mean()

# Plot daily sales and 7-day moving average
plt.figure(figsize=(8,3))

plt.plot(daily_sales['sale_date'], 
         daily_sales['total_sales'], 
         label='Daily Sales', 
         alpha=0.7)

plt.plot(daily_sales['sale_date'], 
         daily_sales['7_day_moving_avg'], 
         label='7-Day Moving Average', 
         color='orange',
         linewidth=2)

# Adjust plot
plt.title('Daily Sales Trends with 7-Day Moving Average')
plt.xlabel('Date')
plt.ylabel('Total Sales ($)')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('line_plot_daily_trend.png')

#%%

# 2) Bar plot total sales with errors

# Group by 'category' to calculate total sales and standard deviation
category_sales = sales_df.groupby('category')['total_sales'].agg(
    ['sum', 'std']).reset_index()

# Plot total sales by category with error bars for standard deviation
plt.figure(figsize=(8, 4))

plt.bar(category_sales['category'], 
        category_sales['sum'], 
        yerr=category_sales['std'], 
        capsize=5, 
        alpha=0.7)

plt.title('Total Sales by Category with Standard Deviation')
plt.xlabel('Category')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', alpha=0.3)
plt.savefig('total_sales_error_bars.png')

# The error bars are difficult to see because they are very small 
# compared to the total sales values.


#%%

# 3) Scatter plot to visualize relashionship 

# Set plot style for better visuals
sns.set(style="whitegrid")

# Create a scatter plot with seaborn
plt.figure(figsize=(8, 4))
scatter_plot = sns.scatterplot(
    data=sales_df,
    x='quantity',
    y='price',
    hue='category',
    alpha=0.7,
    palette='tab10',
    s=50
)

# Adjust plot 
plt.title('Relationship Between Quantity and Price by Category')
plt.xlabel('Quantity')
plt.ylabel('Price ($)')
plt.legend(title='Category', loc='upper right', fontsize='small')
plt.tight_layout()
plt.savefig('relashionship_quantity_price.png')


# Let's analyze the situation:
    
quantity_price = sales_df[['quantity','price']].groupby(
    'quantity').mean().reset_index()
print(quantity_price)

# As we can see in the print below, it is very likely that the price 
# column indicates the unit price of the product, since the price does not 
# vary according to the quantity purchased. Therefore, we can state that 
# there is no relationship between price and quantity, which explains why 
#the points are aligned horizontally in the scatter plot.

#%%

# Visulizing relashionsip between quantity and total sale


sns.set(style="whitegrid")

# Create a scatter plot with seaborn
plt.figure(figsize=(8, 4))
scatter_plot = sns.scatterplot(
    data=sales_df,
    x='quantity',
    y='total_sales',
    hue='category',
    alpha=0.7,
    palette='tab10',
    s=50
)

for category in sales_df['category'].unique():
    category_data = sales_df[sales_df['category'] == category]
    z = np.polyfit(category_data['quantity'], category_data['total_sales'], 1)
    p = np.poly1d(z)
    plt.plot(category_data['quantity'], 
             p(category_data['quantity']),
             label=f'Trend line: {category}',
             linewidth=1.5,
             alpha=0.8)


# Adjust plot 
plt.title('Relationship Between Quantity and Total Sales by Category')
plt.xlabel('Quantity')
plt.ylabel('Total Sales ($)')
plt.legend(loc='upper left', fontsize='small')
plt.tight_layout()
plt.savefig('relashionship_quantity_total_sales.png')

# Now we see a clear trend, as expected, since total sales are a product of 
# quantity and price.