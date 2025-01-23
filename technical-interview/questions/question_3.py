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

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
PATH = os.path.abspath(__file__)
COLORS = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

# Loading the dat unsing pandas
data = pd.read_csv(PATH.replace('/questions/question_3.py','/data/cleaned_sales_data.csv'))

# Line plot of total sales by day
plt.figure(figsize=(20, 6))
daily_sales = data.groupby('sale_date')['price'].sum().reset_index()
daily_sales['moving_average'] = daily_sales['price'].rolling(window=7).mean()
plt.plot(daily_sales['sale_date'], daily_sales['price'], label='Daily Sales', color='purple', alpha=0.5)
plt.plot(daily_sales['sale_date'], daily_sales['moving_average'], label='7-Day Moving Average', color='red', alpha=1)
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20))
plt.gcf().autofmt_xdate()
plt.title('Daily Sales Trends')
plt.legend()
plt.grid()
plt.savefig(PATH.replace('/questions/question_3.py','/data/daily_sales_trends.png'))

# Bar plot of total sales by category
plt.figure(figsize=(20, 6))
plt.rcParams.update({'font.size': 18})
category_sales = data.groupby('category')['price'].sum().reset_index()
category_sales['std'] = data.groupby('category')['price'].std().reset_index()['price']
plt.bar(category_sales['category'], category_sales['price'], yerr= category_sales['std'], capsize=5, color='purple', alpha=0.7)
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.title('Total Sales by Category')
plt.grid()
plt.savefig(PATH.replace('/questions/question_3.py','/data/total_sales_by_category.png'))

# Scatter plot of quantity vs. price
plt.figure(figsize=(10, 6))
plt.rcParams.update({'font.size': 18})
category_colors = dict(zip(data['category'].unique(), COLORS))
data['color'] = data['category'].map(category_colors)
plt.scatter(data['quantity'], data['price'], c=data['color'], alpha=0.5)
# Linear regression
a, b = np.polyfit(data['quantity'], data['price'], 1)
plt.plot(data['quantity'], a*data['quantity'] + b, color='black', label='Trend Line')
plt.xlabel('Quantity')
plt.ylabel('Price')
plt.title('Price vs. Quantity')
plt.legend(loc='upper left')
plt.grid()
plt.savefig(PATH.replace('/questions/question_3.py','/data/quantity_vs_price.png'))