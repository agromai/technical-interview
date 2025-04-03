"""
Question 3: Sales Visualization

Using the cleaned dataset from Question 1 ('sales_data.csv'),
create the following visualizations:

Requirements:
- Use appropriate labels and titles
- Include a legend where necessary
- Use a consistent color scheme
- Save all plots as PNG files

   1. Create a line plot showing daily sales trends over time
      - Include a 7-day moving average line
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

df = pd.read_csv("./technical-interview/data/sales_data_clean1.csv")
df['sale_date'] = pd.to_datetime(df['sale_date'])

df_daily_sales = df.groupby('sale_date')['price'].sum().reset_index()
df_daily_sales['sale_date_num'] = (df_daily_sales['sale_date'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1D')
df_daily_sales['avg_7'] = df_daily_sales['sale_date_num'].rolling(window=7).mean()

print(df_daily_sales.head())

sns.color_palette("muted")
#sns.set_style('whitegrid')

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_daily_sales,
             x='sale_date',
             y='price',
             label='Daily Sales', 
             linewidth=2.5,
             color='#278f65')

sns.lineplot(data=df_daily_sales,
             x='sale_date', 
             y='avg_7',
             label='Avarage (7 days)',
             linewidth=2.5  , 
             color = '#ab4073')

plt.title('Daily sales trends over time', fontsize=16)
plt.xlabel('Data', fontsize=12)
plt.ylabel('Sales', fontsize=12)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('./technical-interview/questions/grafics_question_3/line_plot_question3.png')
plt.close()
#plt.show()

"""
Note:
It's not clear whether price is the total price or the price per unit.
If it's the latter, then quantity should multiply price.
The code can be replaced with:
df['total_price'] = df['price']*df['quantity']
df_grouped_7D = df.groupby(pd.Grouper(key='sale_date', freq='7D'))['total_price'].sum()
"""
"""

2. Create a bar plot showing:
   - Total sales by category
   - Include error bars representing standard deviation
"""

df_sales_category = df.groupby('category').agg(
    total_sales=('price', 'sum'),
    std_dev=('price', 'std')
).reset_index()

print(df_sales_category.head())

plt.figure(figsize=(8, 5))
sns.barplot(
    x='price', 
    y='category', 
    data=df,  
    errorbar='sd', 
    palette='muted'
)

plt.title('Total Sales by Category with Standard Deviation')
plt.xlabel('Total Sales')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig('./technical-interview/questions/grafics_question_3/bar_plot_question3.png')
#plt.show()
plt.close()

"""
3. Create a scatter plot showing:
   - Relationship between quantity and price
   - Color points by category
   - Add a trend line
"""

plt.figure(figsize=(10, 6))



sns.lmplot(
    x='quantity', 
    y='price', 
    hue='category', 
    data=df, 
    palette='muted', 
    ci=None,
    height=6, 
    aspect=1.5,
    legend=False
)

plt.xlabel('Quantity', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.title('Relationship between Quantity and Price by Category', fontsize=14)
plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('./technical-interview/questions/grafics_question_3/scatter_plot_question3.png')
#plt.show()
plt.close()