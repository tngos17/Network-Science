from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from tabulate import tabulate

# Assuming 'df' is your DataFrame
# Create a sample DataFrame for illustration
data = pd.read_csv(r"ALLFLOWMETER_HIKARI2021.csv")
df = pd.DataFrame(data)
df = df.drop('Unnamed: 0.1', axis=1)
df = df.drop('Unnamed: 0', axis=1)
df = df[df['traffic_category'] != 'Background']

# Set display options to show all rows and columns without scientific notation
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)  # Adjust the format as needed

# Replace 'features' with the list of features you want to include in the model SEE FEATURE SELECTION PAGE
features = [
    "originp", "responp", "flow_duration",
    "fwd_pkts_tot", "bwd_pkts_tot", "fwd_data_pkts_tot", "bwd_data_pkts_tot",
    "fwd_pkts_per_sec", "bwd_pkts_per_sec", "flow_FIN_flag_count",
    "fwd_header_size_tot", "fwd_header_size_min", "fwd_header_size_max",
    "bwd_header_size_tot", "bwd_header_size_min", "bwd_header_size_max",
    "flow_FIN_flag_count", "flow_SYN_flag_count", "flow_RST_flag_count",
    "fwd_PSH_flag_count", "bwd_PSH_flag_count", "flow_ACK_flag_count",
    "fwd_URG_flag_count", "bwd_URG_flag_count", "flow_CWR_flag_count",
    "flow_ECE_flag_count", "fwd_pkts_payload.min", "fwd_pkts_payload.max",
    "fwd_pkts_payload.tot", "fwd_pkts_payload.avg", "fwd_pkts_payload.std",
    "bwd_pkts_payload.min", "bwd_pkts_payload.max", "bwd_pkts_payload.tot",
    "bwd_pkts_payload.avg", "bwd_pkts_payload.std", "flow_pkts_payload.min",
    "flow_pkts_payload.max", "flow_pkts_payload.tot", "flow_pkts_payload.avg",
    "flow_pkts_payload.std", "fwd_iat.min", "fwd_iat.max", "fwd_iat.tot",
    "fwd_iat.avg", "fwd_iat.std", "bwd_iat.min", "bwd_iat.max", "bwd_iat.tot",
    "bwd_iat.avg", "bwd_iat.std", "flow_iat.min", "flow_iat.max", "flow_iat.tot",
    "flow_iat.avg", "flow_iat.std", "payload_bytes_per_second",
    "fwd_subflow_pkts", "bwd_subflow_pkts", "fwd_subflow_bytes",
    "bwd_subflow_bytes", "fwd_bulk_bytes", "bwd_bulk_bytes", "fwd_bulk_packets",
    "bwd_bulk_packets", "fwd_bulk_rate", "bwd_bulk_rate", "active.min",
    "active.max", "active.tot", "active.avg", "active.std", "idle.min",
    "idle.max", "idle.tot", "idle.avg", "idle.std", "fwd_init_window_size",
    "bwd_init_window_size", "fwd_last_window_size",
    # Add more features as needed
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

# Interpretations
print("\nInterpretations:")
print('\n')
print(f"- Instances correctly predicted as malicious (TP): {conf_matrix[1, 1]} ({percent_tp:.2f}%)")
print(f"- Instances correctly predicted as benign (TN): {conf_matrix[0, 0]} ({percent_tn:.2f}%)")
print(f"- Instances predicted as malicious but are actually benign (FP): {conf_matrix[0, 1]} ({percent_fp:.2f}%)")
print(f"- Instances predicted as benign but are actually malicious (FN): {conf_matrix[1, 0]} ({percent_fn:.2f}%)")
print('\n')
print(f'Accuracy: {accuracy:.2f}')

# Interpretations
print(confusion_matrix_table)
print('\n')

# Print the results
print('Classification Report:')
print(classification_rep)
