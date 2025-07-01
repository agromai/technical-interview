import pandas as pd

def load_data(filepath):
    """Carrega o CSV para DataFrame e converte datas."""
    try:
        df = pd.read_csv(filepath) #Lê o arquivo CSV
        df['purchase_date'] = pd.to_datetime(df['purchase_date'], errors='coerce') # Converte a coluna de datas para datetime
        print("Arquivo carregado com sucesso.")
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None

def customer_metrics(df):
    """Calcula métricas por cliente."""
    total_gasto = df.groupby('customer_id')['amount'].sum() # Soma tt gasto por cliente
    media_compra = df.groupby('customer_id')['amount'].mean() # Média gasto por cliente
    num_compras = df.groupby('customer_id')['purchase_id'].count() # Número de compras por cliente
    categoria_mais_frequente = df.groupby('customer_id')['category']\
                                .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
    resumo = pd.DataFrame({
        'total_gasto': total_gasto,
        'media_compra': media_compra,
        'num_compras': num_compras,
        'categoria_mais_frequente': categoria_mais_frequente
    })  # Cria DataFrame com todas as métricas calculadas
    return resumo

def top_bottom_customers(resumo, top_n=5):
    """Seleciona top e bottom N clientes por gasto total."""
    ordenado = resumo.sort_values(by='total_gasto', ascending=False) #Ordena por gasto
    top = ordenado.head(top_n) # Top clientes
    bottom = ordenado.tail(top_n) # Bottom clientes
    return top, bottom

def monthly_trends(df):
    """Calcula tendências mensais de compra."""
    df['year_month'] = df['purchase_date'].dt.to_period('M').astype(str) # Extrai ano e mês
    total_vendas = df.groupby('year_month')['amount'].sum() # Soma total de vendas por mês
    valor_medio = df.groupby('year_month')['amount'].mean() # Vaor médio de compra por mês
    tendencias = pd.DataFrame({
        'total_vendas': total_vendas,   
        'valor_medio_compra': valor_medio
        }) # Junta em um DataFrame
    return tendencias

def inactive_customers(df, meses=3):
    """Identifica clientes sem compras nos últimos 3 meses."""
    from pandas.tseries.offsets import DateOffset

    data_max = df['purchase_date'].max() # Ultima data de compra no dataset
    data_limite = data_max - DateOffset(months=meses) # Define limite de tempo
    ultimas_compras = df.groupby('customer_id')['purchase_date'].max() # Última compra por cliente
    inativos = ultimas_compras[ultimas_compras < data_limite].index.tolist() #  Clientes que não compram desde então
    return inativos
    

def main():
    # Caminho para o arquivo CSV
    filepath = 'C:/Users/andressa/OneDrive/Desktop/technical-interview/technical-interview/data/customer_purchases.csv'
    
    # Carrega os dados do CSV
    df = load_data(filepath)
    if df is None:
        print("Não foi possível carregar os dados. Encerrando o programa.")
        return
    # Calcula métricas dos clientes
    resumo = customer_metrics(df)
    print("\nResumo geral dos clientes:")
    print(resumo.head())

    # Top 5 e bottom 5 clientes
    top_5, bottom_5 = top_bottom_customers(resumo)
    print("\nTop 5 clientes por gasto total:")
    print(top_5)
    print("\nBottom 5 clientes por gasto total:")
    print(bottom_5)

    # Tendências mensais
    tendencias = monthly_trends(df)
    print("\nTendências mensais de compra:")
    print(tendencias)

    # Clientes inativos nos últimos 3 meses
    inativos = inactive_customers(df)
    print("\nClientes que não fizeram compras nos últimos 3 meses:")
    for cliente in inativos:
        print(cliente)

# Executa o programa
if __name__ == "__main__":
    main()
