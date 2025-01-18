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
import seaborn as sns

# 1. Line plot showing daily sales trends over time with a 7-day moving average
df1['daily_sales'] = df1['price'] * df1['quantity']
df_daily = df1.groupby('sale_date')['daily_sales'].sum().reset_index()
df_daily['7_day_avg'] = df_daily['daily_sales'].rolling(window=7).mean()

plt.figure(figsize=(10, 6))
plt.plot(df_daily['sale_date'], df_daily['daily_sales'], label='Daily Sales', alpha=0.7)
plt.plot(df_daily['sale_date'], df_daily['7_day_avg'], label='7-Day Moving Average', color='red', linewidth=2)
plt.title('Daily Sales Trends Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.legend()
plt.tight_layout()
plt.savefig('daily_sales_trends.png')
plt.show()


#### 2.
# Calculate total sales by category
category_sales_total = df1.groupby('category')['daily_sales'].sum().reset_index()

# Calculate the standard deviation of daily sales by category
category_sales_std = df1.groupby('category')['daily_sales'].std().reset_index()

# Merge the two pieces of information (sum and standard deviation)
category_sales = pd.merge(category_sales_total, category_sales_std, on='category')
category_sales.columns = ['category', 'total_sales', 'std_dev']

# Create the bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x='category', y='total_sales', data=category_sales, 
            yerr=category_sales['std_dev'], capsize=5, color='skyblue')

# Add title and labels
plt.title('Total Sales by Category with Standard Deviation', fontsize=14)
plt.xlabel('Category', fontsize=12)
plt.ylabel('Total Sales', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

# Plot
plt.show()

