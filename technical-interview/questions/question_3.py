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
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats
from sklearn.linear_model import LinearRegression
import seaborn as sns

# Set style for consistent visualization
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data():
    path = '../output/new_sales_data.csv'
    try:
        df = pd.read_csv(path)

        return df
    
    except FileNotFoundError:
        print(f"File path not found.")
    except Exception as e:
        print(f"Error loading data - {str(e)}")
        return None

def create_daily_sales_trend(df):
    print("\nCreating Daily Sales Trend Line Plot")
    
    # calcular vendas diarias
    if 'quantity' in df.columns:
        df['revenue'] = df['price'] * df['quantity']
        daily_sales = df.groupby('sale_date')['revenue'].sum().reset_index()
    else:
        daily_sales = df.groupby('sale_date')['price'].sum().reset_index()
        daily_sales.columns = ['sale_date', 'revenue']
    
    # calcular media de 7 dias
    daily_sales = daily_sales.sort_values('sale_date')
    daily_sales['moving_avg_7d'] = daily_sales['revenue'].rolling(window=7).mean()
    
    # criar o grafico
    plt.figure(figsize=(14, 8))
    
    plt.plot(daily_sales['sale_date'], daily_sales['revenue'], 
             alpha=0.7, linewidth=1, label='Daily Sales', color='lightblue')
    
    plt.plot(daily_sales['sale_date'], daily_sales['moving_avg_7d'], 
             linewidth=2.5, label='7-Day Moving Average', color='darkblue')
    
    # formatar
    plt.title('Daily Sales Trends Over Time', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Sales Revenue (R$)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('../output/1_daily_sales_trends.png', dpi=300, bbox_inches='tight')
    plt.show()
    

def create_category_sales_revenue(df):
    print("\nCreating Category Sales Revenue Bar Plot")
    
   # calcular receita por transação
    if 'quantity' in df.columns:
        df['revenue'] = df['price'] * df['quantity']
    else:
        df['revenue'] = df['price']

    # calcular total de vendas e desvio padrão por categoria
    category_stats = df.groupby('category')['revenue'].agg(['sum', 'std', 'count']).reset_index()
    category_stats.columns = ['category', 'total_sales', 'std_dev', 'count']
    category_stats['std_dev'].fillna(0, inplace=True) 
    
    # ordenar
    category_stats = category_stats.sort_values('total_sales', ascending=False)

    # criar o grafico
    plt.figure(figsize=(12, 8))
    
    bars = plt.bar(category_stats['category'], category_stats['total_sales'],
                   yerr=category_stats['std_dev'], 
                   capsize=5, 
                   alpha=0.8,
                   edgecolor='black',
                   linewidth=1)
    
    for i, (bar, value) in enumerate(zip(bars, category_stats['total_sales'])):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + category_stats['std_dev'].iloc[i],
                f'R${value:,.0f}', ha='center', va='bottom', fontweight='bold')

    plt.title('Total Sales Revenue by Category', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Total Sales Revenue (R$)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R${x:,.0f}'))
    
    plt.tight_layout()
    plt.savefig('../output/2_category_sales_barplot.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_price_quantity_scatterplot(df):
    print("\nCreating Price vs Quantity Scatter Plot")
    
    # criar o grafico
    plt.figure(figsize=(12, 8))
    
    # setar as cores
    categories = df['category'].unique()
    colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))

    # grafico scatter para cada categoria
    for i, category in enumerate(categories):
        category_data = df[df['category'] == category]
        plt.scatter(category_data['quantity'], category_data['price'],
                   alpha=0.6, s=50, color=colors[i], label=category, edgecolors='black', linewidth=0.5)
    
    # trend line
    x = df['quantity'].values.reshape(-1, 1)
    y = df['price'].values
    
    # linear regression do scikit-learn
    reg = LinearRegression().fit(x, y)
    trend_line = reg.predict(x)
    
    # trend line no grafico
    sort_idx = np.argsort(df['quantity'])
    plt.plot(df['quantity'].iloc[sort_idx], trend_line[sort_idx], 
             color='red', linewidth=2, linestyle='--', alpha=0.8, label='Trend Line')
    
    # calcular a correlation
    correlation = np.corrcoef(df['quantity'], df['price'])[0, 1]
    r_squared = reg.score(x, y)

    plt.text(0.05, 0.95, f'Correlation: {correlation:.3f}\\nR²: {r_squared:.3f}',
             transform=plt.gca().transAxes, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
             verticalalignment='top', fontweight='bold')
    
    plt.title('Relationship between Quantity and Price by Category', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Quantity', fontsize=12)
    plt.ylabel('Price (R$)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R${x:.0f}'))
    
    plt.tight_layout()
    plt.savefig('../output/3_price_quantity_scatterplot.png', dpi=300, bbox_inches='tight')
    plt.show()
    
def create_sales_distribution(df):

    # distribuicao de vendas por categoria
    plt.figure(figsize=(10, 8))
    
    if 'quantity' in df.columns:
        df['revenue'] = df['price'] * df['quantity']
    else:
        df['revenue'] = df['price']
    
    category_totals = df.groupby('category')['revenue'].sum()
    
    plt.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%',
            startangle=90, explode=[0.05] * len(category_totals))
    plt.title('Sales Distribution by Category', fontsize=16, fontweight='bold', pad=20)
    plt.axis('equal')
    
    plt.tight_layout()
    plt.savefig('../output/4_sales_distribution_pie.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    

def main():
   df = load_data()

   create_daily_sales_trend(df)
   create_category_sales_revenue(df)
   create_price_quantity_scatterplot(df)
   create_sales_distribution(df)

   return True

if __name__ == "__main__":
    success = main()