
# Data_Exploration

Download the HIKARI 2021 Dataset from here: https://zenodo.org/records/6463389

You will want the `ALLFLOWMETER_HIKARI2021.csv` and not the `.pcap` files although we will be taking a look at them later.

Next you will want to import the data into your python environment of choice. For this exercise primarily used Jupyter Notebooks however some alternatives like Kaggle can actually handle the entire `.csv'.
As we get to more advances sections of the project we will dive into SQL implementation however, the process above should be fine for now.

# Python Modules

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate
from sklearn.cluster import KMeans,
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
```

###### Data Verification

```python
print(df.columns)

# Show all collumns 
pd.set_option('display.max_columns', 500)

# Basic Descriptive Statistics (Numeric)
df.describe()

# Description (Non-numeric)
df[['title']].describe()

# Column Subset
df[['traffic_category', 'Label', 'originp']]

# Columns containing 'fwd'
df[[c for c in df.columns if 'fwd' in c]]

# Column Subset for traffic_category collumn
df.iloc[:, 84]

#subset as dataframe
df.iloc[:, [84, 85]]

# Only 'traffic_category' containing 'Bruteforce-XML'
df.loc[df['traffic_category'] == 'Bruteforce-XML'] 

# Above plus (AND '&') or (OR '|')
df.loc[df['traffic_category'] == 'Bruteforce-XML'] 
	& (df['originp'] == '13316')
	]
# 
df.loc[df['traffic_category'] == 'Bruteforce-XML'] 

# Value counts of each categorical variable for 'traffic_category'
df[['traffic_category', 'Label']].value_counts()

# Group by
df.groupby('traffic_category')[['fwd_pkts_tot']].agg(['mean','min','max'])

# Assign new columns
df['newcolumn'] = df['original_column'] \ 60

# Sorting data

df[['traffic_category']].sort_values('flow_duration')
```


# Visualizations
```python

#Bar Chart
import matplotlib.pyplot as plt

df[['traffic_category', 'Label']].value_counts().plot(kind='bar')
plt.xlabel('Traffic Category')
plt.ylabel('Count')
plt.show()

# Interactive Bar Chart for Background/Benign & Malicious
# Toatals (n)
label_counts = df['Label'].value_counts()
label_counts_with_values = df.groupby('Label')['traffic_category'].value_counts().unstack().fillna(0)
print(label_counts)

print(label_counts_with_values)

# Basic Correlation Heatmap
plt.figure(figsize=(15, 5))
sns.heatmap(label_counts_with_values, annot=True, cmap='viridis', fmt='g', vmin=10000, vmax=3279)
plt.title('Frequency of Each Label and Corresponding Values in Another Column')
plt.show()

# Box Chart
label_counts_with_values.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Frequency of Each Label and Corresponding Values in Another Column')
plt.xlabel('Label')
plt.ylabel('Count')
plt.legend(title="Traffic Category", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Correlation Heatmap
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
numeric_df = df[numeric_columns]
plt.figure(figsize=(12, 10))
correlation_matrix = numeric_df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", annot_kws={"size": 3})
plt.title('Correlation Heatmap', pad=15)
plt.xticks(rotation=45, ha='right')  # Align x-axis labels to the right for better readability
plt.yticks(rotation=0)  # Keep y-axis labels horizontal
plt.tight_layout()
plt.show()

# Correlation Heatmap with Outliers
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
numeric_df = df[numeric_columns]
plt.figure(figsize=(20, 15))
correlation_matrix = numeric_df.corr()
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
f, ax = plt.subplots(figsize=(15, 12))
sns.heatmap(correlation_matrix, mask=mask, cmap='coolwarm', annot=True, fmt=".2f", annot_kws={"size": 4})
plt.title('Correlation Heatmap with Outliers Highlighted', pad=20)  # Increase pad for better title spacing
plt.show()
```

---
# Interpretations

###### Basic Heatmap

Correlation Values:

The numbers in the boxes represent the correlation coefficients between pairs of numeric columns in the dataset. Correlation coefficients range from -1 to 1, indicating the strength and direction of the linear relationship between variables. 
```
  1: Perfect positive correlation   
 -1: Perfect negative correlation 
  0: No correlation Color Coding:
```
###### Correlation Heatmap with Outliers
1. **Correlation Values:**
    
    - The numbers in the boxes represent the correlation coefficients between pairs of numeric columns in your dataset.
    - The range of correlation values is from -1 to 1, where:
        - 1 indicates a perfect positive correlation (as one variable increases, the other also increases),
        - -1 indicates a perfect negative correlation (as one variable increases, the other decreases),
        - 0 indicates no correlation.
2. **Color Coding:**
    
    - The colors represent the strength and direction of the correlation:
        - Darker shades indicate stronger correlation (either positive or negative).
        - Lighter shades or no color (white) indicate weaker or no correlation.
3. **Upper Triangle:**
    
    - The heatmap is often symmetrical, and the upper triangle is a mirror image of the lower triangle.
    - It only displays half of the matrix to avoid redundancy.
4. **Mask:**
    
    - The white triangular mask on the upper side helps to focus on the lower triangle, making the plot less cluttered.
    - Values in the masked area are not calculated or shown.
5. **Outliers Highlighted:**
    
    - In the modified plot, I added a mask to highlight the outliers (values beyond a certain threshold).
    - Outliers might be interesting to investigate further as they could indicate unusual relationships between variables.
6. **Interpreting Specific Values:**
    
    - Focus on values close to 1 or -1 for potentially strong relationships.
    - Values close to 0 suggest weak or no correlation.
    - Positive values indicate a positive relationship, while negative values indicate a negative relationship.
