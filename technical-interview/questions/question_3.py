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

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Carrega os dados
csv = pd.read_csv(r"technical-interview\data\sales_data_cleaned.csv")


# Agrupar datas
vendas_diarias = csv.groupby('datetime')['quantity'].sum()
medias_semanais = []
datas_medias = []
check = 0
soma= 0

# Computar média movel
for i in range(len(vendas_diarias.index)):
   if check == 7:
      medias_semanais.append(soma/7)
      datas_medias.append(vendas_diarias.index[i])
      check = 0
      soma = 0
   soma += vendas_diarias.values[i]
   check += 1


# Criar plot de linhas
fig= plt.figure(figsize=(10, 5))
plt.plot(vendas_diarias.index,vendas_diarias.values,linewidth=0.1,label="Vendas diárias")
plt.plot(datas_medias,medias_semanais,linewidth=0.5,c='k',label="Média de vendas semanal")
plt.xticks(datas_medias[::len(datas_medias)//3])
plt.title("Vendas ao longo do tempo")
plt.xlabel("Datetime")
plt.ylabel("Quantidade vendida")
plt.legend()
plt.ylim(0,10)
plt.savefig("technical-interview/data/lineplot.png")
plt.close()


# Computar total de vendas para cada categoria
vendas_por_categoria = csv.groupby('category')['quantity'].sum()

# Computar o erro da soma de N variáveis aleatórias
variaveis_por_categoria = csv.groupby('category')['quantity'].count()
erro_por_variável = csv.groupby('category')['quantity'].std()

erro_por_categoria = np.sqrt(variaveis_por_categoria * erro_por_variável.values**2)


# Cores por categoria
cores = {vendas_por_categoria.index[i]:f"C{i}" for i in range(len(vendas_por_categoria.index))}

# Criar plot de barras
fig= plt.figure(figsize=(10, 5))
barra = plt.bar(vendas_por_categoria.index,vendas_por_categoria.values, color=[cores[i] for i in vendas_por_categoria.index])

plt.errorbar(vendas_por_categoria.index,vendas_por_categoria.values,erro_por_categoria,barsabove=True,
             color='k', ls='None',label='Desvio padrão', capsize=10)

plt.title("Total de Vendas por categoria")
plt.legend()
plt.ylim(800,1200)
plt.savefig("technical-interview/data/barplot.png")
plt.close()


# Agrupar quantidades, categorias e preços
preco_por_quantidade = csv.groupby(['quantity', 'category'])['price'].mean().reset_index()


# Criar plots scatter
fig= plt.figure(figsize=(10, 5))

for categoria, cor in cores.items():
   filtro = preco_por_quantidade[preco_por_quantidade['category']==categoria]
   plt.scatter(filtro['quantity'], filtro['price'], color=cor, label=categoria)
   
   # Criar aproximação linear
   a, b = np.polyfit(filtro['quantity'],filtro['price'],1)
   plt.plot(filtro['quantity'],a*filtro['quantity'] + b, color=cor)

plt.ylabel("Média de preço")
plt.xlabel("Quantidade")
plt.title("Preço por quantidade")
plt.legend()
plt.savefig("technical-interview/data/scatterplot.png")
plt.close()