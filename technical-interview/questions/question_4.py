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

import scipy.stats as stats


df1 = pd.read_csv('sales_data.csv') # loading dataframe

df1['price'].fillna(mean_price, inplace=True)  # imputing mean on NA values 
mode_category = df1['category'].mode()[0] # getting the mode value
df1['category'].fillna(mode_category, inplace=True) # imputing the mode on NA values
df1['sale_date'] = pd.to_datetime(df1['sale_date']) # convert 'sale_date' to datetime


##### 1.
def perform_anova_or_kruskal(df):
    try:
        # Check if the 'price' column is normally distributed using the Shapiro-Wilk test
        stat, p_value = stats.shapiro(df['price'])
        
        if p_value < 0.05:
            print(f"Warning: The 'price' column does not have a normal distribution (p-value = {p_value:.4f})")
            print("Performing Kruskal-Wallis test instead of ANOVA...")
            
            # If normality is rejected, perform Kruskal-Wallis test (non-parametric)
            categories = df['category'].unique()
            kruskal_result = stats.kruskal(*(df[df['category'] == category]['price'] for category in categories))
            return "Kruskal-Wallis", kruskal_result.statistic, kruskal_result.pvalue
        
        else:
            print(f"The 'price' column has a normal distribution (p-value = {p_value:.4f})")
            
            # If normality assumption is satisfied, perform the one-way ANOVA test
            categories = df['category'].unique()
            anova_result = stats.f_oneway(*(df[df['category'] == category]['price'] for category in categories))
            return "ANOVA", anova_result.statistic, anova_result.pvalue
        
    except Exception as e:
        print(f"Error: {e}")

perform_anova_or_kruskal(df1)
test_type, test_statistic, test_pvalue = perform_anova_or_kruskal(df1)
print(f"Test Type: {test_type}")
print(f"Statistic: {test_statistic}, p-value: {test_pvalue}")


# Detecting outliers using Z-scores
def detect_outliers(df):
    try:
        z_scores = stats.zscore(df['price'])
        outliers = df[np.abs(z_scores) > 3]
        print(f"Potential outliers (z-score > 3):\n{outliers}")
        
        # Optionally, visualize the outliers
        plt.figure(figsize=(8, 6))
        sns.boxplot(x='category', y='price', data=df)
        plt.title('Outliers in Price by Category')
        plt.show()
        
    except Exception as e:
        print(f"Error detecting outliers: {e}")

detect_outliers(df1)


##### 2.
"""
   def perform_chi_square(data):
       observed = data.groupby(['category', 'status']).size()  
       chi2, p_value = stats.chi2_contingency(observed)
       return chi2, p_value
The the column 'status' don't exist in the dataset from Question 1. Besides, the current code is trying to directly pass the observed values from the groupby result (that is a Series) to the stats.chi2_contingency() function,
 but chi2_contingency expects a contingency table.
"""

# Possible solution:
def perform_chi_square(data, col1, col2):
    contingency_table = pd.crosstab(data[col1], data[col2])
    chi2, p_value= stats.chi2_contingency(contingency_table)
        
    return chi2, p_value

