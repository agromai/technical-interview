"""
Question 2: Customer Purchase Analysis

Using the provided dataset 'customer_purchases.csv', perform the following analyses:

1. Calculate the following metrics per customer:
   - Total amount spent
   - Average purchase value
   - Number of purchases
   - Most frequently bought category

2. Create a summary DataFrame with:
   - Top 5 customers by total spend
   - Bottom 5 customers by total spend

3. Calculate the monthly purchase trends:
   - Total sales per month
   - Average purchase value per month

Bonus: Identify any customers who haven't made a purchase in the last 3 months
"""

import pandas

dataPur = pandas.read_csv("../data/customer_purchases.csv")
print(dataPur)

# 1. Calculate the following metrics per customer:
print(sum(dataPur['amount']))  # 101993.11

print(dataPur['amount'].mean())   # 101.99311

print(len(dataPur['amount']))   # 1000

print(dataPur['category'].mode()[0])  # Home & Garden


# 2. Create a summary DataFrame with:
cinco_top = dataPur.sort_values('amount', ascending=False).head(5)
print(cinco_top)

cinco_bott = dataPur.sort_values('amount', ascending=True).head(5)
print(cinco_bott)

# 3. Calculate the monthly purchase trends:
# - Total sales per month
dataPur['purchase_date'] = pandas.to_datetime(dataPur['purchase_date'])
dataPur['mes'] = dataPur['purchase_date'].dt.to_period('M')
print(dataPur)

# - Total sales per month
vendas_mesT = dataPur.groupby('mes')['amount'].sum()
print(vendas_mesT)

# - Average purchase value per month
vendas_mesMedia = dataPur.groupby('mes')['amount'].mean()
print(vendas_mesMedia)



