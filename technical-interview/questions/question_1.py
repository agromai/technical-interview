"""
Question 1: Data Cleaning and Basic Analysis

Using the provided dataset 'sales_data.csv', perform the following tasks:

1. Load and examine the dataset
2. Clean the data:
   - Handle missing values in the 'price' column (replace with mean)
   - Handle missing values in the 'category' column (replace with mode)
   - Convert 'sale_date' to datetime
3. Create a summary of:
   - Total number of sales per category
   - Average price per category
   - Number of missing values handled

The cleaned dataset should be ready for further analysis.
"""

# Your code here

import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
from datetime import datetime

# Carrega os dados
csv = pd.read_csv(r"technical-interview\data\sales_data.csv")

# Cálculo de média e moda
media = csv['price'].mean()
moda = csv['category'].mode()

# Contador de faltas
missing = 0

# Substituir as faltas e datetime
for i in range(len(csv['category'])):
   if type(csv['category'][i]) == float:
      csv.loc[i,'category'] = moda[0]
      missing += 1
   
   if csv['price'][i] == None:
      csv.loc[i,'price'] = media
      missing +=1

   ano, mes, dia = csv['sale_date'][i].split("-")
   csv.loc[i,'sale_date'] = datetime.combine(date(int(ano), int(mes), int(dia)), datetime.min.time())

# Substitui coluna sale_date por datetime
csv.rename(columns={'sale_date':'datetime'},inplace=True)

# Agrupamento de valores pela categoria
vendas_por_categoria = csv.groupby('category')['quantity'].sum()
preco_por_categoria = csv.groupby('category')['price'].mean()

# Salvar dataset em csv limpo
csv.to_csv("technical-interview\data\sales_data_cleaned.csv")

# Criação dos plots
fig, ax = plt.subplots(1, 3, figsize=(15, 6))

barra = ax[0].bar(vendas_por_categoria.index,vendas_por_categoria.values)
ax[0].set_ylabel("Total de Vendas")
ax[0].tick_params(axis='x', rotation=45)
ax[0].bar_label(barra)

barra1 = ax[1].bar(preco_por_categoria.index,preco_por_categoria.values)
ax[1].set_ylabel("Preço Médio")
ax[1].tick_params(axis='x', rotation=45)
ax[1].bar_label(barra1)

ax[2].pie([missing,len(csv['category'])-missing],labels=[f"Dados faltantes: {missing}", f"Restante: {len(csv['category'])-missing}"])
plt.tight_layout()
plt.show()