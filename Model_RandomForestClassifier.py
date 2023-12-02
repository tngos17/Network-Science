# Commit message: Improved data preprocessing and added RandomForestClassifier model

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from tabulate import tabulate

# Assuming 'df' is your DataFrame
# Create a sample DataFrame for illustration
data = pd.read_csv(r"ALLFLOWMETER_HIKARI2021.csv")

# Drop unnecessary columns
df = df.drop('Unnamed: 0.1', axis=1)
df = df.drop('Unnamed: 0', axis=1)

df = pd.DataFrame(data)

# Set display options to show all rows and columns without scientific notation
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)  # Adjust the format as needed

# Assuming 'features' and 'target' are defined
# Replace 'features' with the list of features you want to include in the model
features = [
    # List of features...
]

target = 'Label'

X = df[features]
y = df[target]

# Use 'traffic_category' as the stratifying variable
stratify_var = df['traffic_category']

# Split the data into training and testing sets, preserving the distribution of 'Label'
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=stratify_var)

# Standardize the features (optional but can be beneficial for some algorithms)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create a Random Forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

# Calculate total instances
total_instances = len(y_test)

# Calculate percentages
percent_tp = (conf_matrix[1, 1] / total_instances) * 100
percent_tn = (conf_matrix[0, 0] / total_instances) * 100
percent_fp = (conf_matrix[0, 1] / total_instances) * 100
percent_fn = (conf_matrix[1, 0] / total_instances) * 100

# Define the confusion matrix information with percentages
confusion_matrix_info = [
    ["True Positives (TP)", conf_matrix[1, 1], f"{percent_tp:.2f}%"],
    ["True Negatives (TN)", conf_matrix[0, 0], f"{percent_tn:.2f}%"],
    ["False Positives (FP)", conf_matrix[0, 1], f"{percent_fp:.2f}%"],
    ["False Negatives (FN)", conf_matrix[1, 0], f"{percent_fn:.2f}%"],
    ["Total Instances", total_instances, "100.00%"]
]

# Print the confusion matrix table
confusion_matrix_table = tabulate(confusion_matrix_info, headers=["Metric", "Count", "Percentage"], tablefmt="pretty")
print(confusion_matrix_table)

# Print the results
print(f'Accuracy: {accuracy:.2f}')
print('Confusion Matrix:')

# Print the confusion matrix table
confusion_matrix_table = tabulate(confusion_matrix_info, headers=["Metric", "Count", "Percentage"], tablefmt="pretty")
print(confusion_matrix_table)

# Interpretations
print("\nInterpretations:")
print(f"- Instances correctly predicted as malicious (TP): {conf_matrix[1, 1]} ({percent_tp:.2f}%)")
print(f"- Instances correctly predicted as benign (TN): {conf_matrix[0, 0]} ({percent_tn:.2f}%)")
print(f"- Instances predicted as malicious but are actually benign (FP): {conf_matrix[0, 1]} ({percent_fp:.2f}%)")
print(f"- Instances predicted as benign but are actually malicious (FN): {conf_matrix[1, 0]} ({percent_fn:.2f}%)")

print('Classification Report:')
print(classification_rep)


