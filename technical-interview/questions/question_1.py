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
import pandas
# 1
dataSale = pandas.read_csv("../data/sales_data.csv")
print(dataSale)

valores_ausentes = dataSale.isna().sum()
print("Valores ausentes antes o tratamento:\n", valores_ausentes)  # 30+49 = 79 NaN

# 2
print(dataSale['price'][1])
media = sum(dataSale['price'])/len(dataSale['price'])
print(media)
# df['Idade'] = df['Idade'].fillna(df['Idade'].mean())
dataSale['price'] = dataSale['price'].fillna(dataSale['price'].mean())
print(dataSale['price'])

category_mode = dataSale['category'].mode()[0]  # mode()[0} retorna nome com maior frequencia 
dataSale['category'] = dataSale['category'].fillna(category_mode)
print(dataSale['category'])

# df['sele_date'] = pd.to_datetime(df['sele_date'])
dataSale['sale_date'] = pandas.to_datetime(dataSale['sale_date'])
print(dataSale['sale_date'])

# 3
vendas_Cat = dataSale.groupby('category')['quantity'].sum()
print(vendas_Cat)
preco_Cat = dataSale.groupby('category')['price'].mean()
print(preco_Cat)

valores_ausentes = dataSale.isna().sum()
print("Valores ausentes após o tratamento:\n", valores_ausentes)  # antes tratamento: linha 26






