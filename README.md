# Network-Science
Data Science on Network Traffic Data!

Understanding network traffic is one of the most pressing issues to the information security professional. In this exercise I will be using the HIKARI 2021 data set to demonstraite some basic machine learning models as well as go over the techniques ued to get there. I had a lot of fun doing this and hope you will enjoy it as well!

# Project Flow Chart
![Project Outline_](https://github.com/tngos17/Network-Science/assets/64931318/f4348a9c-994c-493e-8d2d-81bbbf08275d)

# Importing the Data
Download the HIKARI 2021 Dataset from here: https://zenodo.org/records/6463389

To read the full publication visit: https://www.mdpi.com/2076-3417/11/17/7868/htm#B9-applsci-11-07868

You will want the `ALLFLOWMETER_HIKARI2021.csv` and not the .pcap files although we will be taking a look at them later.

Next you will want to import the data into your python environment of choice. For this exercise primarily used Jupyter Notebooks however some alternatives like Kaggle can actually handle the entire `.csv`. As we get to more advances sections of the project we will dive into SQL implementation however, the process above should be fine for now.

# A First Glance 

## Data Features (HIKARI-2021)
Here is a short list of features implemented by the dataset. For a full view visit the `Data_Features` page. To better understand and appreciate their selection I highly recommend reading the full publication. Some of these features will need to be excluded from our model such as uid and IP information to avoid obvious prediction correlation for those variables.

| No  | Feature                        | Description                                         |
|----|--------------------------------|-----------------------------------------------------|
| 1  | uid                            | Unique identifier for each record.                   |
| 2  | originh                        | Source host of the network flow.                     |
| 3  | originp                        | Source port of the network flow.                     |
| 4  | responh                         | Destination host of the network flow.                |
| ...|  | | |
| 85 | traffic_category                | Category of network traffic.                       |
| 86 | Label                           | The label assigned to the network flow, possibly indicating normal or malicious activity.|

# Target Variables

Below are the potential values for the `traffic_category` variable. The goal here is to create a model which can distinguish and predict between 
1. Background data (i.e. network traffic which may or maynot contain malicious traffic)
2. Benign data (i.e. syntethic traffic known to be non-mailicious)
3. Malicious data (i.e. known malicious traffic conforming to the types listed below)

| traffic_category    | Label | Count  |
| ------------------- | ----- | ------ |
| Benign              | 0     | 347431 |
| Background          | 0     | 170151 |
| Probing             | 1     | 23388  |
| Bruteforce          | 1     | 5884   |
| Bruteforce-XML      | 1     | 5145   |
| XMRIGCC CryptoMiner | 1     | 3279   |

Lets visualize the types of traffic used in the data set using `pandas`.
![download](https://github.com/tngos17/Network-Science/assets/64931318/af6001bc-ca25-4cd4-b377-77a5452d8fc5)

The HIKARI dataset takes a reasonable approach by focusing on the application layer and utalizes a small variety of Malicious data to generate data. Unfortunately, the ratio of bad traffic to benign is problematic from a modeling perspective however, this is a problem that will be addressed at a later point as we are only in the pre-processing stage of this exercise.
![Bar Chart](https://github.com/tngos17/Network-Science/assets/64931318/8f1301f4-dea8-4104-a1f0-a1533da6952d)

# Focusing on Target Variables

For now, lets determine some basic variables of interest. In order to select interesting variables we can take examine their variance and eliminate features on the lower end. This is a common technique of geature selection for preprocessing a machine learning model.

![download](https://github.com/tngos17/Network-Science/assets/64931318/bd78a255-34b8-4ba1-a858-e521fbb62c9f)

As we can see varience drops quite heavily, so lets narrow it down a little. 

![download](https://github.com/tngos17/Network-Science/assets/64931318/0eb4db1f-bb10-472d-befe-eb9e57b478bd)

Another interesting visualization is the deploy the Pearson Correlation Heatmap. Pearson correlation ranges from -1 to 1, where 1 indicates a perfect positive correlation, -1 indicates a perfect negative correlation, and 0 indicates no correlation. Looking at the top values (closer to 1), it seems that certain pairs of variables have a very strong positive correlation. For example, the variables `fwd_iat.tot` and `flow_iat.tot` have a correlation coefficient of 1.00, indicating a perfect positive correlation, which makes sense as they self identify. Similarly, `flow_iat.max` and `idle.max` also have a perfect positive correlation.

For building a predictive model, we should consider variables that have a strong correlation with the target variable or with each other. However, keep in mind that correlation does not imply causation, and further analysis or experimentation may be needed to understand the relationships. Fancy as it looks, this kind of specification is more of an exploritory element than a true benefit in terms of model fit.

![download](https://github.com/tngos17/Network-Science/assets/64931318/17bfadfc-f321-4931-a593-d065d9b6a1d8)

Variables with 0.99 or 0.98 Correlation: `flow_iat.avg`, `fwd_iat.avg`, and `flow_iat.min`
Variables with 0.97 or 0.96 Correlation: `active.std` and `active.max``idle.min` and `idle.avg`
Variables with 0.95 or 0.94 Correlation: `bwd_iat.max`, `idle.max`, `fwd_iat.max`
Variables with 0.93 or 0.91 Correlation: `fwd_iat.std`, `bwd_iat.std`, `flow_iat.max`, `idle.max`
Variables with 0.90 or 0.88 Correlation: `fwd_iat.std`, `flow_iat.max`, `idle.max`
Variables with 0.87 or 0.86 Correlation: `flow_iat.std`, `idle.max`, `fwd_iat.max`

Almost all of these correlations are due to statistical self-reference and should highlight the potential value of implementing raw  `pcap` files for training data. Although the `HIKARI 2021` data has released such data which will be examined at a later point, let us continue to try and make sense of modeling a dataset which can be so publicly available due to its reshaping of features to make use of its anonymity.

# Initial Model - Random Forest Classifier

![Diagram (1)](https://github.com/tngos17/Network-Science/assets/64931318/baa695f0-af25-4f9c-9b79-da23048a265c)

Using a basic random forest classifier we are returned a rough model. By playing around with a cocktail of features and model arraingements I was able to get the following model specifications to an baseline accuracy of 0.84. We have yet to accoount for many of the traditional hurdles which may present our findings as more descriptive of our features than the actual targets.

|        Metric        | Count | Percentage |
|----------------------|-------|------------|
| True Positives (TP)  |  963  |   1.25%    |
| True Negatives (TN)  | 63785 |   82.81%   |
| False Positives (FP) | 5702  |   7.40%    |
| False Negatives (FN) | 6576  |   8.54%    |
|   Total Instances    | 77026 |  100.00%   |

Interpretations:

- Instances correctly predicted as malicious (TP): 963 (1.25%)
- Instances correctly predicted as benign (TN): 63785 (82.81%)
- Instances predicted as malicious but are actually benign (FP): 5702 (7.40%)
- Instances predicted as benign but are actually malicious (FN): 6576 (8.54%)

Unsuprizingly the issue lies in the models ability to appropriately classify and accturately predict malicious traffic. We should recall the overall shape and skew of the data towards `Label = 0` traffic as a potential cause for concern. More importantly, we must also consider the logistical useability of such a model. In the future I will be taking raw `.pcap` files from the same data source to use as training data hosted in an SQL database. Once that is done and I am satisfied with a more robustly developed machine learning model we can begin deploying our model on live network traffic! 

Classification Report:
```
              precision    recall  f1-score   support

           0       0.91      0.92      0.91     69487
           1       0.14      0.13      0.14      7539

    accuracy                           0.84     77026
   macro avg       0.53      0.52      0.52     77026
weighted avg       0.83      0.84      0.84     77026
```
![download](https://github.com/tngos17/Network-Science/assets/64931318/698dddc7-daf0-43cf-858d-b0d1f3515d35)

