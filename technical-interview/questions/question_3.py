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
from question_1 import Q1
from  matplotlib import pyplot as plt
import seaborn as sns


class Q3:
    def __init__(self):
        self._data = Q1()
        self._data = self._data.get_data()
        self._line_plot()
        self._bar_plot()
        self._scatter_plot()

    def _line_plot(self):
        sales_trends = (
            self._data.groupby("sale_date")
            .apply(lambda x: (x["price"] * x["quantity"]).sum())
            .reset_index()
        )
        sales_trends.columns = ["sale_date", "total_sales"]
        sales_trends = (
            self._data.groupby("sale_date")
            .apply(lambda x: (x["price"] * x["quantity"]).sum())
            .reset_index()
        )
        sales_trends.columns = ["sale_date", "total_sales"]
        sales_trends['moving_avg'] = sales_trends['total_sales'].rolling(window=7).mean()
        plt.figure(figsize=(12, 6))
        plt.plot(
            sales_trends["sale_date"],
            sales_trends["total_sales"],
            label="Daily Sales",
            color="blue",
        )
        plt.plot(
            sales_trends["sale_date"],
            sales_trends["moving_avg"],
            label="7-Day Moving Average",
            color="orange",
        )
        plt.title("Daily Sales Trends with 7-Day Moving Average")
        plt.xlabel("Date")
        plt.ylabel("Total Sales ($)")
        plt.legend()
        plt.grid(True)
        plt.savefig("daily_sales_trends.png")

    def _bar_plot(self):
        category_sales = (
            self._data.groupby("category")
            .apply(lambda x: (x["price"] * x["quantity"]).sum())
            .reset_index()
        )
        category_sales.columns = ["category", "total_sales"]
        category_std = (
            self._data.groupby("category")
            .apply(lambda x: (x["price"] * x["quantity"]).std())
            .reset_index()
        )
        category_std.columns = ["category", "std_dev"]
        category_sales = category_sales.merge(category_std, on="category")
        plt.figure(figsize=(25, 15))
        plt.bar(
            category_sales["category"],
            category_sales["total_sales"],
            yerr=category_sales["std_dev"],
            capsize=5,
            color="skyblue",
        )
        plt.title("Total Sales by Category with Standard Deviation")
        plt.xlabel("Category")
        plt.ylabel("Total Sales ($)")
        plt.xticks(rotation=45)
        plt.grid(axis="y")
        plt.savefig("sales_by_category.png")

    def _scatter_plot(self):
        plt.figure(figsize=(25, 15))
        sns.scatterplot(
            data=self._data,
            x="quantity",
            y="price",
            hue="category",
            palette="viridis",
            alpha=0.8,
        )
        plt.title("Relationship Between Quantity and Price")
        plt.xlabel("Quantity")
        plt.ylabel("Price ($)")
        plt.legend(title="Category")
        plt.grid(True)
        plt.savefig("scatter_quantity_price.png")
