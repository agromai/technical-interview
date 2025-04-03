"""
Question 4: Statistical Analysis and Error Handling

Using scipy and the cleaned dataset from Question 1, perform the following tasks:

1. Implement error handling for the following analyses:
   - Perform a one-way ANOVA test to compare prices across different categories
   - Calculate and plot the confidence intervals for mean prices in each category
   - Identify potential outliers using z-scores
   
2. Debug and fix the following code snippet that attempts to perform a chi-square test:
   ```python
   def perform_chi_square(data):
       observed = data.groupby(['category', 'status']).size()
       chi2, p_value = stats.chi2_contingency(observed)
       return chi2, p_value
   
3. Implement proper logging to track:
   - Any statistical assumptions violations
   - Data type mismatches
   - Invalid calculations

Your solution should be robust against various edge cases and include appropriate error messages.
"""

import logging
from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import sys

# Configure the logger
logging.basicConfig(filename='./technical-interview/questions/questions_outputs_logs/logs_question_4.log',  # Log file
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Message format
)

# Redirect print output to a file
output_file = './technical-interview/questions/questions_outputs_logs/output_question_4.txt'
with open(output_file, 'w') as f:
    sys.stdout = f  # Redirect stdout to the file

    try:
        # Load the dataset
        df = pd.read_csv('./technical-interview/data/sales_data_clean1.csv')
        logging.info("Dataset successfully loaded.")
        print("Dataset successfully loaded.")
    except FileNotFoundError as e:
        logging.error(f"Error loading the dataset: {e}")
        print(f"Error loading the dataset: {e}")
        raise

    # 1. ANOVA Test
    try:
        df_price_category = [df_temp['price'].values for _, df_temp in df.groupby('category')]
        if len(df_price_category) < 2:
            raise ValueError("ANOVA test requires at least two categories for comparison.")
        
        f_stat, p_value = stats.f_oneway(*df_price_category)
        logging.info(f"ANOVA test successfully performed. F-Statistic: {f_stat}, P-Value: {p_value}")
        print(f"ANOVA test successfully performed. F-Statistic: {f_stat}, P-Value: {p_value}")
    except ValueError as e:
        logging.error(f"Error in ANOVA test: {e}")
        print(f"Error in ANOVA test: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in ANOVA test: {e}")
        print(f"Unexpected error in ANOVA test: {e}")

    # 1. Confidence Intervals
    try:
        df_summary = df.groupby('category')['price'].agg(['mean', 'count', 'std']).reset_index()
        df_summary['ci_lower'] = df_summary['mean'] - 1.96 * (df_summary['std'] / np.sqrt(df_summary['count']))
        df_summary['ci_upper'] = df_summary['mean'] + 1.96 * (df_summary['std'] / np.sqrt(df_summary['count']))
        
        plt.figure(figsize=(10, 6))
        plt.errorbar(df_summary['category'], df_summary['mean'], 
                     yerr=[df_summary['mean'] - df_summary['ci_lower'], 
                           df_summary['ci_upper'] - df_summary['mean']], 
                     fmt='o', capsize=5, color='salmon')
        plt.title('Confidence intervals for mean prices in each category')
        plt.xlabel('Category')
        plt.ylabel('Mean Price')
        plt.savefig('./technical-interview/questions/grafics_question_4/ci_mean_prices.png')
        plt.close()
        logging.info("Confidence intervals successfully calculated and plotted.")
        print("Confidence intervals successfully calculated and plotted.")
    except KeyError as e:
        logging.error(f"Error calculating confidence intervals: missing column in the dataset: {e}")
        print(f"Error calculating confidence intervals: missing column in the dataset: {e}")
    except Exception as e:
        logging.error(f"Unexpected error calculating confidence intervals: {e}")
        print(f"Unexpected error calculating confidence intervals: {e}")

    # 1. Identify potential outliers using z-scores
    try:
        df['z_score'] = (df['price'] - df['price'].mean()) / df['price'].std()
        df_outliers = df[np.abs(df['z_score']) > 3]
        logging.info(f"Outliers successfully identified. Total outliers: {len(df_outliers)}")
        print('\nPotential outliers (z-scores > 3):\n')
        print(df_outliers[['category', 'price', 'z_score']].sort_values(by='z_score', ascending=False))
        print('\nBoth sales should be checked manually.\nSale 999 is significantly higher than the others.\nSale 975 is significantly lower than the others.\n')
    except KeyError as e:
        logging.error(f"Error calculating z-scores: missing column in the dataset: {e}")
        print(f"Error calculating z-scores: missing column in the dataset: {e}")
    except Exception as e:
        logging.error(f"Unexpected error calculating z-scores: {e}")
        print(f"Unexpected error calculating z-scores: {e}")
        
    # 2. Chi-Square Test
    print('\nDebugging and fixing the chi-square test code snippet:\n',
          'The code attempts to create a contingency table using the groupby method, but it does not create a proper contingency table.',
          'The chi2_contingency function requires a 2D array or DataFrame as input.',
          'Chi-squere tests only categorical variables, so we need to ensure that the data is categorical.',
          'However, this dataframe does not have a column named "status", and only have one categorical variable.', 
          'Therefore, we cant perform a chi-square test on this dataset.',sep='\n')

    print('If status were on this dataset, the correct aplication would be', 
          'contingency_table = pd.crosstab(df[category], df[status])',
          'from scipy.stats import chi2_contingency',
          'chi2, p_value, dof, expected = chi2_contingency(contingency_table)',sep='\n')

    print('Interpratation of the chi-square test results:',
          'If the p-value is less than the significance level (e.g., 0.05), we reject the null hypothesis, indicating a significant association between the two categorical variables.',
          'If the p-value is greater than the significance level, we fail to reject the null hypothesis, indicating no significant association between the two categorical variables.',sep='\n')

# Restore stdout to default
sys.stdout = sys.__stdout__
print(f"Output has been written to {output_file}.")

