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
   ```

3. Implement proper logging to track:
   - Any statistical assumptions violations
   - Data type mismatches
   - Invalid calculations

Your solution should be robust against various edge cases and include appropriate error messages.
"""

# from scipy import stats
# import pandas as pd
# import logging
# import matplotlib.pyplot as plt
# import numpy as np
# from question_1 import df

# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def perform_anova(df):
#     try:
#         if 'category' not in df.columns or 'price' not in df.columns:
#             raise KeyError("Missing 'category' or 'price' columns in the dataset.")

#         grouped_data = [group['price'].dropna() for _, group in df.groupby('category')]
#         if len(grouped_data) < 2:
#             raise ValueError("Not enough groups to perform ANOVA.")

#         # Perform ANOVA
#         f_stat, p_value = stats.f_oneway(*grouped_data)
#         logging.info("ANOVA Test Completed Successfully")
#         return f_stat, p_value
#     except Exception as e:
#         logging.error(f"Error during ANOVA: {e}")
#         return None, None


# def calculate_plot_confidence_intervals(df, confidence=0.95):
#     try:
#         if 'category' not in df.columns or 'price' not in df.columns:
#             raise KeyError("Missing 'category' or 'price' columns in the dataset.")

#         means, errors = [], []
#         categories = df['category'].unique()

#         for category in categories:
#             prices = df.loc[df['category'] == category, 'price'].dropna()
#             mean = np.mean(prices)
#             stderr = stats.sem(prices)
#             ci = stats.t.interval(confidence, len(prices)-1, loc=mean, scale=stderr)
#             means.append(mean)
#             errors.append(mean - ci[0])

#         # Plotting
#         plt.figure(figsize=(10, 6))
#         plt.bar(categories, means, yerr=errors, capsize=5, color='skyblue', edgecolor='black')
#         plt.title('Mean Prices with Confidence Intervals by Category', fontsize=16)
#         plt.xlabel('Category', fontsize=12)
#         plt.ylabel('Mean Price', fontsize=12)
#         plt.tight_layout()
#         plt.savefig('confidence_intervals.png')
#         plt.show()
#     except Exception as e:
#         logging.error(f"Error during Confidence Interval Calculation: {e}")

# def detect_outliers(df, column, threshold=3):
#     try:
#         if column not in df.columns:
#             raise KeyError(f"Column '{column}' does not exist in the dataset.")

#         z_scores = stats.zscore(df[column].dropna())
#         outliers = df[np.abs(z_scores) > threshold]
#         logging.info(f"Found {len(outliers)} potential outliers in column '{column}'.")
#         return outliers
#     except Exception as e:
#         logging.error(f"Error during Outlier Detection: {e}")
#         return pd.DataFrame()
