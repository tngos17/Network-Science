
# Data Importation

Download the HIKARI 2021 Dataset from here: https://zenodo.org/records/6463389

You will want the `ALLFLOWMETER_HIKARI2021.csv` and not the `.pcap` files although we will be taking a look at them later.

Next you will want to import the data into your python environment of choice. For this exercise primarily used Jupyter Notebooks however some alternatives like Kaggle can actually handle the entire `.csv'.
As we get to more advances sections of the project we will dive into SQL implementation however, the process above should be fine for now.

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
