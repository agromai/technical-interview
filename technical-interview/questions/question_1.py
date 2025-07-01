import pandas as pd


def load_data(filepath):
    """ 
    Carrega o CSV para um DataFrame.
    
    Parâmetros:
    - filepath (str): Caminho do arquivo CSV.

    Retorna:
    - pd.DataFrame: DataFrame com os dados carregados.
    - None: se ocorrer algum erro.
    """
    try:
        df = pd.read_csv(filepath) # Tenta carregar o CSV
        print("Arquivo carregado com sucesso.")
        return df 
    except FileNotFoundError:
        print(f"Erro: O arquivo {filepath} não foi encontrado.")
        return None 
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None 

# Caminho do arquivo CSV
filepath = 'C:/Users/andressa/OneDrive/Desktop/technical-interview/technical-interview/data/sales_data.csv'

# Carrega o dataset usando a função
df = load_data(filepath)
 

# Verifica se o carregamento do dataFrame foi correto
if df is None:
    print("Não foi possível carregar o arquivo.")
    exit()  # Se não conseguiu carregar, o código para aqui

# Exibe as primeiras 20 linhas para inspeção inicial
print("Primeiras 20 linhas do dataset:")
print(df.head(20), '\n')

# Exibe informações gerais do DataFrame (tipos, valores nulos, etc)
print("Informações do dataset:")
print(df.info(), '\n')


#  Início do tratamento dos dados


# Conta valores ausentes na coluna 'price
missing_price = df['price'].isnull().sum()
# Calcula média dos preços para substituir valores ausentes
price_mean = df['price'].mean()
# Substitui valores ausentes em 'price' pela média calculada
df['price'] = df['price'].fillna(price_mean)


# Conta valores ausentes na coluna 'category'
missing_category = df['category'].isnull().sum()
# Calcula moda da coluna 'category' para substituir valores ausentes
category_mode = df['category'].mode()[0]
# Substitui valores ausentes emna coluna 'category' pela moda calculada
df['category'] = df['category'].fillna(category_mode)


# Converte 'sale_date' para o tipo datetime
# Se algum valor não puder ser convertido, vira NaT (equivalente a Nan para datas)
df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')


#  Análise dos dados

# Conta total de vendas por categoria
sales_per_category = df['category'].value_counts()

# Calcula o preço médio por categoria
avg_price_per_category = df.groupby('category')['price'].mean()

# Soma total dos valores ausentes tratados nas colunas 'price' e 'category'
total_missing_handled = missing_price + missing_category

# Resultados finais

print("Total de vendas por categoria:")
print(sales_per_category, '\n')

print("Preço médio por categoria:")
print(avg_price_per_category, '\n')

print(f"Total de valores ausentes tratados: {total_missing_handled}")
