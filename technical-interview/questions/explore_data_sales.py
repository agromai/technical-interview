# Script para exploração inicial dos dados

import pandas as pd
df = pd.read_csv("./technical-interview/data/sales_data.csv")
print(df.head(), df.info(),df.describe(),df.isnull().sum(),sep="\n")
print("Os resultados indicam que os tipos das variáveis estão adequados, exceto para sales_date.\nApenas price e category apresentam valores vazios.\nA análise superficial da média e da mediana indica que a distribuição não apresenta outliers preocupantes,\na variância e os percentis de 25% e 75% são coerentes, indicando uma distribuição normal.\nOs valores mínimos e máximos parecem razoáveis.")

print("Percentual de valores nulos em price:\n",100*df['price'].isna().sum()/df['price'].size)

print("Valor da moda de category: ",df['category'].mode()[0])

print(df['category'].value_counts())