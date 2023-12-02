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

Lets visualize the types of traffic used in the data set using `pandas`.

![download](https://github.com/tngos17/Network-Science/assets/64931318/af6001bc-ca25-4cd4-b377-77a5452d8fc5)

| traffic_category    | Label | Count  |
| ------------------- | ----- | ------ |
| Benign              | 0     | 347431 |
| Background          | 0     | 170151 |
| Probing             | 1     | 23388  |
| Bruteforce          | 1     | 5884   |
| Bruteforce-XML      | 1     | 5145   |
| XMRIGCC CryptoMiner | 1     | 3279   |
