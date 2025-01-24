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
import matplotlib.pyplot as plt
from scipy.stats import linregress
from question_1 import df
import numpy as np

# Group by day to calculate daily sales
daily_sales = df.groupby(df['sale_date'].dt.date)['quantity'].sum()

# Calculate a 7-day moving average
daily_sales_7day_ma = daily_sales.rolling(window=7).mean()

# Plot the daily sales trend
plt.figure(figsize=(12, 6))
plt.plot(daily_sales.index, daily_sales, label='Daily Sales', color='blue', alpha=0.6)
plt.plot(daily_sales_7day_ma.index, daily_sales_7day_ma, label='7-Day Moving Average', color='orange', linewidth=2)
plt.title('Daily Sales Trends', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Sales', fontsize=12)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('plots/daily_sales_trend.png')
plt.show()

# Group by category to calculate total sales and standard deviation
category_stats = df.groupby('category')['quantity'].agg(['sum', 'std']).reset_index()

# Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(
    category_stats['category'], 
    category_stats['sum'], 
    yerr=category_stats['std'], 
    capsize=5, 
    color='skyblue', 
    edgecolor='black'
)
plt.title('Total Sales by Category', fontsize=16)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Total Sales', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('plots/total_sales_by_category.png')
plt.show()

# Create the scatter plot
plt.figure(figsize=(10, 6))
categories = df['category'].unique()
colors = plt.cm.tab10(range(len(categories)))

# Plot each category in the scatter plot
for cat, color in zip(categories, colors):
    cat_data = df[df['category'] == cat]
    plt.scatter(cat_data['quantity'], cat_data['price'], label=cat, alpha=0.7, color=color)

# Add a trend line
slope, intercept, r_value, p_value, std_err = linregress(df['quantity'], df['price'])
x_vals = np.linspace(df['quantity'].min(), df['quantity'].max(), 100)
y_vals = slope * x_vals + intercept
plt.plot(x_vals, y_vals, color='red', linestyle='--', label='Trend Line')

# Add labels, legend, and title
plt.title('Quantity vs. Price by Category', fontsize=16)
plt.xlabel('Quantity', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.legend(title='Category')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('plots/quantity_vs_price_scatter.png')
plt.show()
