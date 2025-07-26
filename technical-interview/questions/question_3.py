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

# Your code here

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import os

cwd = os.getcwd()

# Load Dataset
sales_path = os.path.join(cwd, "technical-interview/data/cleaned_sales_data.csv")
sales_dataset = pd.read_csv(sales_path)

# Daily sales trends over time
daily_sales = sales_dataset.groupby('sale_date')['quantity'].sum().reset_index()
daily_sales['7_day_avg'] = daily_sales['quantity'].rolling(window=7).mean()

plt.plot(daily_sales['sale_date'], daily_sales['quantity'], label='Daily Sales', alpha=0.5)
plt.plot(daily_sales['sale_date'], daily_sales['7_day_avg'], label='7-Day Moving Average', color='red', linewidth=2)

plt.title('Daily Sales Trend')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.legend()
plt.savefig('sales_over_time.png')
plt.show()

# Bar Plot: Total Sales per category

category = ['Books','Clothing', 'Electronics','Home & Garden', 'Sports']
quantity = np.array(sales_dataset.groupby('category')['quantity'].count())
error_std = sales_dataset.groupby('category')['quantity'].count().std()

fig,ax = plt.subplots()
bar_labels = ['red', 'blue', 'green', 'orange', 'gray']
bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:gray']

ax.bar(category, quantity, yerr=error_std, align='center', ecolor='black', capsize=10, label=bar_labels, color=bar_colors)
ax.set_ylabel('Total Sales')
ax.set_title('Total sales by category')

plt.savefig('sales_per_category.png')
plt.show()