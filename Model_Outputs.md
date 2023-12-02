# Random Forest Classifier Output

Interpretations:

- Instances correctly predicted as malicious (TP): 963 (1.25%)
- Instances correctly predicted as benign (TN): 63785 (82.81%)
- Instances predicted as malicious but are actually benign (FP): 5702 (7.40%)
- Instances predicted as benign but are actually malicious (FN): 6576 (8.54%)

Accuracy: 0.84
+----------------------+-------+------------+
|        Metric        | Count | Percentage |
+----------------------+-------+------------+
| True Positives (TP)  |  963  |   1.25%    |
| True Negatives (TN)  | 63785 |   82.81%   |
| False Positives (FP) | 5702  |   7.40%    |
| False Negatives (FN) | 6576  |   8.54%    |
|   Total Instances    | 77026 |  100.00%   |
+----------------------+-------+------------+

Classification Report:
              precision    recall  f1-score   support

           0       0.91      0.92      0.91     69487
           1       0.14      0.13      0.14      7539

    accuracy                           0.84     77026
   macro avg       0.53      0.52      0.52     77026
weighted avg       0.83      0.84      0.84     77026

![Bar Chart](https://github.com/tngos17/Network-Science/assets/64931318/cdd26e32-d0ac-446f-95bd-c153d5cc6316)
