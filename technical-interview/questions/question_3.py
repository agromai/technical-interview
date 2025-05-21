"""
Question 3: Sales Visualization

Using the cleaned dataset from Question 1 ('sales_data.csv'), create the following visualizations: OK

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

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

path_csv = os.path.join(os.getcwd(),'..','data','sales_data.csv')
file = pd.read_csv(path_csv)

file['price'] = file['price'].fillna(file['price'].mean())

file['category'] = file['category'].fillna(file['category'].mode()[0])

file['sale_date'] = pd.to_datetime(file['sale_date'], errors='coerce')

daily_sales = file.groupby('sale_date')['price'].sum().sort_index()
daily_sales = daily_sales.sort_index()
avr_7_days = daily_sales.rolling(window=7).mean()

# Plot daily sales and 7-day moving average
plt.figure(figsize=(12,5))
plt.plot(daily_sales, label='Daily Sales')
plt.plot(avr_7_days, label='7-Day Moving Average')
plt.title('Daily Sales and 7-Day Moving Average')
plt.xlabel('Date')
plt.ylabel('Daily Sales')
plt.legend()
plt.savefig('daily_sales.png') 
plt.close()

file['total_sales'] = file['price'] * file['quantity']
sales_by_category = file.groupby('category')['total_sales'].agg(['sum', 'std']).reset_index()

# Plot total sales by category with error bars showing standard deviation
plt.title('Total Sales by Category')
plt.figure(figsize=(8,5))
plt.bar(sales_by_category['category'],sales_by_category['sum'],yerr=sales_by_category['std'])
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.savefig('sales_by_category.png')
plt.close() 

colors = ['green', 'blue', 'green', 'pink', 'violet']  
categories = file['category'].unique() 
plt.figure(figsize=(8,5)) 

for i, c in enumerate(categories): 
   category_data = file[file['category'] == c] 
   plt.scatter(category_data['quantity'], category_data['price'], color=colors[i % len(colors)], label=c)

# Plot scatter points of price vs quantity, colored by category
plt.title('Price vs Quantity by Category')
plt.xlabel('Quantity') 
plt.ylabel('Price') 
plt.legend(title='Category')
plt.savefig('price_vs_quantity_by_category.png')

# This scatter plot shows the relationship between price and quantity, with points colored by category, but does not include a trend line