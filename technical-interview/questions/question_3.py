import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configura estilo dos gráficos
sns.set(style="whitegrid", palette="pastel")


def load_data(filepath):
    """
    Carrega os dados do arquivo CSV, converte a coluna de datas e remove linhas com dados faltando.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    df = pd.read_csv(filepath)

    required_cols = ['sale_date', 'price', 'category', 'quantity']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"O CSV precisa conter as colunas: {', '.join(required_cols)}")

    df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')

    # Remove linhas com dados faltando nas colunas essenciais
    df = df.dropna(subset=required_cols)

    return df


def save_plot(fig, filename, title):
    """
    Salva o gráfico em PNG e imprime uma confirmação.
    """
    fig.tight_layout()
    fig.savefig(filename)
    print(f"📊 {title} salvo como {filename}")
    plt.close(fig)


def plot_daily_sales(df):
    """
    Cria um gráfico de vendas diárias com média móvel de 7 dias.
    """
    daily_sales = df.groupby('sale_date')['price'].sum().reset_index()
    daily_sales['7d_ma'] = daily_sales['price'].rolling(window=7).mean()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_sales['sale_date'], daily_sales['price'], label='Vendas Diárias')
    ax.plot(daily_sales['sale_date'], daily_sales['7d_ma'], label='Média Móvel (7 dias)', linewidth=3)
    ax.set_title('Tendência Diária de Vendas')
    ax.set_xlabel('Data')
    ax.set_ylabel('Total de Vendas')
    ax.legend()

    save_plot(fig, 'daily_sales_trends.png', 'Gráfico de Vendas Diárias')


def plot_sales_by_category(df):
    """
    Cria gráfico de barras com as vendas por categoria. 
    """
    category_stats = df.groupby('category').agg({'price': ['sum', 'std']})
    category_stats.columns = ['total_sales', 'std_dev']
    category_stats = category_stats.sort_values('total_sales', ascending=False).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=category_stats, x='category', y='total_sales', ax=ax, yerr=category_stats['std_dev'])
    ax.set_title('Vendas Totais por Categoria')
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Total de Vendas')
    ax.tick_params(axis='x', rotation=45)

    save_plot(fig, 'sales_by_category.png', 'Gráfico de Vendas por Categoria')


def plot_quantity_vs_price(df):
    """
    Cria gráfico de dispersão mostrando quantidade vendida vs preço.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='quantity', y='price', hue='category', alpha=0.7, s=60, edgecolor='w', linewidth=0.5, ax=ax)
    sns.regplot(data=df, x='quantity', y='price', scatter=False, color='gray', line_kws={"linewidth": 2}, ax=ax)
    ax.set_title('Relação entre Quantidade e Preço')
    ax.set_xlabel('Quantidade')
    ax.set_ylabel('Preço')
    ax.legend(title='Categoria', loc='upper right')

    save_plot(fig, 'quantity_vs_price.png', 'Gráfico de Dispersão Quantidade vs Preço')


def main():
    """
    Função principal que carrega os dados e gera os gráficos.
    """
    filepath = '../data/sales_data.csv'
  

    try:
        df = load_data(filepath)
        plot_daily_sales(df)
        plot_sales_by_category(df)
        plot_quantity_vs_price(df)
        print("✅ Todos os gráficos foram gerados com sucesso.")
    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
