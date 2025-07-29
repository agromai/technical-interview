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

# Your code here

import matplotlib.pyplot as plt
import pandas as pd
from datetime import date

# Carrega os dados
csv = pd.read_csv(r"technical-interview\data\customer_purchases.csv")

# Métricas do consumidor:
gasto_total = csv.groupby('customer_id')['amount'].sum().sort_values()
gasto_medio = csv.groupby('customer_id')['amount'].mean()
numero_compras = csv.groupby('customer_id')['purchase_id'].count()
categoria_preferida = csv.groupby('customer_id')['category'].aggregate(lambda x: x.mode()[0])


# Criação do sumário com maiores e menores gastos
sumario = pd.DataFrame({'top_customer':reversed(gasto_total.index[-5:]), 'top_amount': reversed(gasto_total.values[-5:]), 'bottom_customer': gasto_total.index[:5], 'bottom_amount': gasto_total.values[:5]})

# Impressão do sumário
print("=========================Summary=========================")
print(sumario)
print("=========================================================")

# Conversão de string para data
for i in range(len(csv['purchase_date'])):
   ano, mes, dia = csv['purchase_date'][i].split("-")
   csv.loc[i,'purchase_date'] = date(int(ano), int(mes), int(dia))
   csv.loc[i,'purchase_month'] = date(int(ano), int(mes), 1)

# Análise mensal
numero_compras_mensal = csv.groupby('purchase_month')['purchase_id'].count()
gasto_mensal = csv.groupby('purchase_month')['amount'].mean()
clientes_mensais = csv.groupby('purchase_month')['customer_id']

# Detectar clientes ausentes nos últimos meses
faltantes = set()
for id in csv['customer_id'].unique():
   mes1, mes2, mes3 = sorted(clientes_mensais.groups.keys())[-3:]

   if id in clientes_mensais.get_group(mes1) or id in clientes_mensais.get_group(mes2) or id in clientes_mensais.get_group(mes3):
      continue
   else:
      faltantes.add(id)

print(f"Clientes que ausentes nos últimos 3 meses: {faltantes}")


# Criação dos plots
fig, ax = plt.subplots(2, 1, figsize=(15, 6))

barra = ax[0].bar(numero_compras_mensal.index,numero_compras_mensal.values)
ax[0].set_ylabel("Total de Vendas")
ax[0].tick_params(axis='x', rotation=45)
ax[0].bar_label(barra)

barra1 = ax[1].bar(gasto_mensal.index,gasto_mensal.values)
ax[1].set_ylabel("Venda Média")
ax[1].tick_params(axis='x', rotation=45)
ax[1].bar_label(barra1)
ax[1].set_ylim(90,110)

plt.tight_layout()
plt.show()