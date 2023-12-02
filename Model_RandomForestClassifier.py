# Commit message: Improved data preprocessing and added RandomForestClassifier model

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

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

# Print the results
print(f'Accuracy: {accuracy:.2f}')
print('Confusion Matrix:')
print(conf_matrix)
print('Classification Report:')
print(classification_rep)
