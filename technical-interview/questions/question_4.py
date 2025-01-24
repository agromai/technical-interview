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

#%%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm
import scipy.stats as stats


#%%

# Functions

def perform_anova(dataframe, category_col, value_col):
    """
    

    Parameters
    ----------
    dataframe : pandas DataFrame
        The classes to compare.
    category_col : str
        Categories to compare.
    value_col : str
        Values to compare.

    Raises
    ------
    ValueError
        If less than two categories are input.

    Returns
    -------
    f_stat
        The f-statistic for ANOVA test.
    p_value
        The p-value for ANOVA test.

    """
    
    # Error handling for ANOVA
    try:
        # Check if there are at least two unique categories
        unique_categories = dataframe[category_col].nunique()
        if unique_categories < 2:
            raise ValueError(
                "There must be at least two unique categories for ANOVA test.")

        # Group data by category and extract prices
        groups = [group[value_col].values for 
                  j, group in dataframe.groupby(category_col)]

        # Perform one-way ANOVA
        f_stat, p_value = stats.f_oneway(*groups)
        return f_stat, p_value
    except Exception as e:
        return str(e)

def calculate_confidence_intervals(dataframe, category_col, value_col, 
                                   confidence=0.95):
    """
    

    Parameters
    ----------
    dataframe : pandas DataFrame
        DataFrame with the columns to evaluate..
    category_col : str
        Category column.
    value_col : str
        Value to analyze.
    confidence : float, optional
        DESCRIPTION. The default is 0.95.

    Returns
    -------
    pandas DataFrame
        Dataframe with the confidence intervals.

    """
    
    summary = []
    for category, group in dataframe.groupby(category_col):
        mean = group[value_col].mean()
        std = group[value_col].std()
        n = len(group[value_col])
        
        # Standard error
        sdt_error = std / np.sqrt(n)  
        
        # Z-score for the given confidence level
        z = norm.ppf(1 - (1 - confidence) / 2)  
        ci_lower = mean - z * sdt_error
        ci_upper = mean + z * sdt_error
        summary.append((category, mean, ci_lower, ci_upper))
    return pd.DataFrame(summary, columns=["Category", "Mean", 
                                          "CI Lower", "CI Upper"])

def clean_display(info):
    """

    Parameters
    ----------
    info : str
        The information to be printed.

    Returns
    -------
    None.

    """
    print("#"*79)
    print(info.center(79))
    print("#"*79,"\n")

#%% 

# OBS.: I decided to use the same file and clean the dataset again to avoid
# exporting the cleaned dataset to another CSV and creating an additional 
# file.

# Load the dataset
file_path = '../data/sales_data.csv'
sales_df = pd.read_csv(file_path)
sales_df_bckp = sales_df.copy() # Separate copy of the df if necessary

#%%

# Cleaning the data

# Replace with mean the missing values in the 'price' column 
price_mean = sales_df['price'].mean()
sales_df['price'] = sales_df['price'].fillna(price_mean)


# Replace with mode the missing values in the 'category' column 
category_mode = sales_df['category'].mode()[0]
sales_df['category'] =  sales_df['category'].fillna(category_mode)

# Convert 'sale_date' column to datetime format 
sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])

#%%

###############################################################################
# 1) PERFORMING ANALYSIS AND HANDLING ERRORS                                    
############################################################################### 


# ANOVA TEST
anova_result = perform_anova(sales_df, 'category', 'price')

print("ANOVA TEST RESULTS")
print("F-statistic:", anova_result[0])
print("P-value:", anova_result[1])

# Since the p-value is greater than the typical threshold of 0.05, we CANNOT
# reject the null hypothesis (that prices are the same across categories). 
# Therefore, we can say that there is no statistically significant 
# difference in the prices across the different categories.

#%%

###############################################################################
# 1) PERFORMING ANALYSIS AND HANDLING ERRORS                                    
############################################################################### 


# CONFIDENCE NTERVALS

conf_intervals = calculate_confidence_intervals(sales_df, "category", "price")

# Plot confidence intervals
plt.figure(figsize=(8, 4))
plt.errorbar(
    conf_intervals['Category'],
    conf_intervals['Mean'],
    yerr=[
        conf_intervals['Mean'] - conf_intervals['CI Lower'],
        conf_intervals['CI Upper'] - conf_intervals['Mean']
    ],
    fmt="o",
    color="red",
    capsize=5,
    capthick=2,
)
plt.title("Confidence Intervals for Mean Prices by Category")
plt.xlabel("Category")
plt.ylabel("Price ($)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#%%

###############################################################################
# 1) PERFORMING ANALYSIS AND HANDLING ERRORS                                    
############################################################################### 

# POTENTIAL OUTLIERS USING Z-SCORES

sales_df["z_score"] = (
    sales_df["price"] - sales_df["price"].mean()) / sales_df["price"].std()

# Is outlier if z-score > 3 or < -3
outliers = sales_df[np.abs(sales_df["z_score"]) > 3]

clean_display("POTENTIAL PRICE OUTLIERS")
print(outliers)

#%% 

###############################################################################
# 2) DEBUGGING AND FIXING  CODE SNIPPET                                   
############################################################################### 



def perform_chi_square(data):
    
    observed = data.groupby(['category', 'status']).size()
    
    # Let's verify this observed object
    print(observed)
    print(observed.shape)
    
    # 1º ERROR (Not a bug, but it does not return the correct values for 
    # the test):     
    # A contingency table is a structure (e.g., a DataFrame or NumPy array)
    # where rows and columns represent categories, and the cell values are 
    # the counts. The "observed" dataframe is summary of counts in the 
    # form of a 6-dimensional pandas Series object
    
    # Let's now create a proper contingency table
    observed = pd.crosstab(data['category'], data['status'])
    
    # chi2, p_value = stats.chi2_contingency(observed)
    
    # 2º ERROR:     
    # chi2, p_value = stats.chi2_contingency(observed)
    # ValueError: too many values to unpack (expected 2)
    # Let's look at the documentation of the the chi2_contingency function
    
    print(help(stats.chi2_contingency),"\n")
    
    # As we can see, it returns an object containing four attributes and 
    # the code tries to unpack only 2. To fix this, we can take the four 
    # attributes returned by the function but keep only the ones that we
    # need
    
    chi2, p_value, _, _= stats.chi2_contingency(observed)
    return chi2, p_value

data = pd.DataFrame({
    'category': ['A', 'A', 'B', 'B', 'C', 'C', 'C'],
    'status': ['success', 'fail', 'success', 'fail', 'success', 
               'fail', 'success']
})

# Perform chi-square test
chi2, p_value = perform_chi_square(data)
clean_display("PERFORMING THE CHI-2 TEST CORRECTLY")
print(f"Chi-square statistic: {round(chi2,2)}, P-value: {round(p_value,2)}")


 


