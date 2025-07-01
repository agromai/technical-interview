# Technical Interview

Welcome to our technical interview assessment! This repository contains a series of questions designed to evaluate your Python programming skills and data analysis capabilities.

## Setup Instructions

1. Clone this repository
2. Create a virtual environment:
   ```bash
     # you can use any virtual environment manager you want, but we recommend using conda
   conda create -n technical-interview python=3.11
   conda activate technical-interview
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Interview Structure

The interview consists of 4 questions, focusing on:
1. Data Cleaning and Basic Analysis
2. Data Manipulation and Aggregation
3. Data Visualization
4. Advanced Analytics and Machine Learning

### For Junior Role Candidates
- Complete questions 1-3
- Question 4 is optional/bonus

### For Data Scientist Role Candidates
- Complete all questions 1-4

## Questions Overview

### Question 1: Data Cleaning and Basic Analysis
Work with sales data to demonstrate your ability to handle missing values and perform basic statistical analysis.

### Question 2: Data Manipulation and Aggregation
Show your skills in transforming and aggregating data to derive meaningful insights.

### Question 3: Data Visualization
Create informative visualizations to communicate data insights effectively.

### Question 4: Advanced Analytics (Required for Data Scientists, Bonus for Juniors)
Apply advanced statistical methods and machine learning techniques to solve a complex business problem.

## Submission Guidelines

1. Create a new branch with your name: `firstname-lastname`
2. Complete the questions in their respective Python files
3. Commit your changes and push to your branch
4. Create a pull request with your solutions

## Evaluation Criteria

- Code quality and organization
- Problem-solving approach
- Documentation and comments
- Accuracy of results
- Efficiency of solutions
- Proper use of Git

## Time Limit

- 24 hours from the time you get the email from the recruiter.

Good luck!

---


## Your Solutions

### Questão 1: Data Cleaning and Basic Analysis

Para a questão 1, realizei as seguintes etapas:

- Implementei a função `load_data()` com tratamento de exceções para carregar o CSV com segurança.
- Preenchi valores ausentes da coluna `price` com a **média** da coluna.
- Preenchi valores ausentes da coluna `category` com a **moda** (categoria mais frequente).
- Converti a coluna `sale_date` para o tipo `datetime`, com tratamento de erro silencioso (`errors='coerce'`).
- Exibi as 20 primeiras linhas e as informações básicas do DataFrame.
- Calculei:
  - Total de vendas por categoria (`value_counts`)
  - Preço médio por categoria (`groupby`)
  - Total de valores ausentes tratados

O código foi comentado e organizado por seções.

### Alterações no `requirements.txt`

Atualizei o arquivo `requirements.txt` com versões mais recentes das bibliotecas usadas no projeto, visando compatibilidade e estabilidade:

**Arquivo anterior (original):**    

pandas==1.3.3
numpy==1.21.2
scipy==1.7.1
matplotlib==3.4.3
scikit-learn==0.24.2
statsmodels==0.12.2


**Novo arquivo atualizado:**  

pandas==2.2.2
numpy==1.26.4
scipy==1.13.1
matplotlib==3.8.4
scikit-learn==1.4.2
statsmodels==0.14.1


Essas versões foram utilizadas com sucesso no ambiente virtual criado com `venv`, sem o uso do `conda`, e foram compatíveis com o script desenvolvido para a questão 1.


### Questão 2: Manipulação e Análise de Dados

Nesta parte do desafio, trabalhei com dados de compras de clientes para entender melhor o comportamento de consumo.

Organizei o código em funções para facilitar a leitura e o reuso. As principais etapas foram:

- **`load_data()`**  
  Carrega os dados do CSV e converte a coluna de datas para o formato correto (`datetime`). Também trata erros caso o arquivo não seja encontrado.

- **`customer_metrics()`**  
  Calcula para cada cliente:
  - Total gasto
  - Valor médio por compra
  - Número total de compras
  - Categoria mais comprada

- **`top_bottom_customers()`**  
  Retorna os 5 clientes que mais gastaram e os 5 que menos gastaram.

- **`monthly_trends()`**  
  Mostra como as vendas variaram ao longo dos meses (total e média).

- **`inactive_customers()`**  
  Identifica clientes que não fizeram compras nos últimos 3 meses.

Mantive o código limpo, comentado e fácil de executar para quem quiser testar.


---