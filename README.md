![Diagram (1)](https://github.com/tngos17/Network-Science/assets/64931318/baa695f0-af25-4f9c-9b79-da23048a265c)# Network-Science
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


Using a basic random forest classifier we are returned a rough model. By playing around with a cocktail of features and model arraingements I was able to get the following model specifications to an baseline accuracy of 0.84. We have yet to accoount for many of the traditional hurdles which may present our findings as more descriptive of our features than the actual targets.

|        Metric        | Count | Percentage |
|----------------------|-------|------------|
| True Positives (TP)  |  963  |   1.25%    |
| True Negatives (TN)  | 63785 |   82.81%   |
| False Positives (FP) | 5702  |   7.40%    |
| False Negatives (FN) | 6576  |   8.54%    |
|   Total Instances    | 77026 |  100.00%   |

![Diagram (1)](https://github.com/tngos17/Network-Science/assets/64931318/ac27734b-baa9-4b76-b143-cf9984b8c22a)

Interpretations:

- Instances correctly predicted as malicious (TP): 963 (1.25%)
- Instances correctly predicted as benign (TN): 63785 (82.81%)
- Instances predicted as malicious but are actually benign (FP): 5702 (7.40%)
- Instances predicted as benign but are actually malicious (FN): 6576 (8.54%)

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

![Uploading <svg version="1.1" baseProfile="full" width="1076.0" height="300.0" viewbox="0 0 1076 300" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ev="http://www.w3.org/2001/xml-events">
		<desc >#.ML: fill=#c3c3c3 dashed
	#.box: fill=#8f8 dashed
	#.left: alight=left
	
	
	
	  [All Traffic] --&gt; [Label = 0]
	  [All Traffic] --&gt; [Label = 1]
	  [Label = 0] --&gt; [Benign]
	  [Label = 0] --&gt; [Background]
	  [Label = 1] --&gt; [Known Malicioous]
	  [Known Malicioous] --&gt; [Probing]
	  [Known Malicioous] --&gt; [Bruteforce]
	  [Known Malicioous] --&gt; [Brutefore-XML]
	  [Known Malicioous] --&gt; [XMRIGCC CryptoMiner]
	  [Background] --&gt; [Potentially Malicious]
	  [Background] --&gt; [Potentially Benign]
	
	
	</desc>
	<g stroke-width="1.0" text-align="left" font="12pt Helvetica, Arial, sans-serif" font-size="12pt" font-family="Helvetica" font-weight="bold" font-style="normal">
			<g font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" stroke-width="3.0" stroke-linejoin="round" stroke-linecap="round" stroke="#33322E">
				<g stroke="transparent" fill="transparent">
					<rect x="0.0" y="0.0" height="300.0" width="1076.0" stroke="none"></rect>
				</g>
			<g transform="translate(8, 8)" fill="#33322E">
					<g transform="translate(20, 20)" fill="#33322E" font-family="Helvetica" font-size="12pt" font-weight="normal" font-style="normal">
						<g stroke-dasharray="6 6">
							<path d="M297.5 22.8 L124.75 51 L124.75 64.33333333333333 L124.8 64.3 " fill="none"></path>
						</g>
					<path d="M119.4 57.7 L124.8 64.3 L130.1 57.7 L124.8 71.0 Z"></path>
					<g stroke-dasharray="6 6">
							<path d="M386.5 20.6 L650.5 51 L650.5 64.33333333333333 L650.5 64.3 " fill="none"></path>
						</g>
					<path d="M645.2 57.7 L650.5 64.3 L655.8 57.7 L650.5 71.0 Z"></path>
					<g stroke-dasharray="6 6">
							<path d="M96.5 102.0 L60 122 L60 135.33333333333334 L60.0 135.3 " fill="none"></path>
						</g>
					<path d="M54.7 128.7 L60.0 135.3 L65.3 128.7 L60.0 142.0 Z"></path>
					<g stroke-dasharray="6 6">
							<path d="M153.0 102.0 L189.5 122 L189.5 135.33333333333334 L189.5 135.3 " fill="none"></path>
						</g>
					<path d="M184.2 128.7 L189.5 135.3 L194.8 128.7 L189.5 142.0 Z"></path>
					<g stroke-dasharray="6 6">
							<path d="M650.5 102.0 L650.5 122 L650.5 135.33333333333334 L650.5 135.3 " fill="none"></path>
						</g>
					<path d="M645.2 128.7 L650.5 135.3 L655.8 128.7 L650.5 142.0 Z"></path>
					<g stroke-dasharray="6 6">
							<path d="M572.5 171.2 L448 193 L448 206.33333333333334 L448.0 206.3 " fill="none"></path>
						</g>
					<path d="M442.7 199.7 L448.0 206.3 L453.3 199.7 L448.0 213.0 Z"></path>
					<g stroke-dasharray="6 6">
							<path d="M617.3 173.0 L574.5 193 L574.5 206.33333333333334 L574.5 206.3 " fill="none"></path>
						</g>
					<path d="M569.2 199.7 L574.5 206.3 L579.8 199.7 L574.5 213.0 Z"></path>
					<g stroke-dasharray="6 6">
							<path d="M683.7 173.0 L726.5 193 L726.5 206.33333333333334 L726.5 206.3 " fill="none"></path>
						</g>
					<path d="M721.2 199.7 L726.5 206.3 L731.8 199.7 L726.5 213.0 Z"></path>
					<g stroke-dasharray="6 6">
							<path d="M728.5 167.6 L925 193 L925 206.33333333333334 L925.0 206.3 " fill="none"></path>
						</g>
					<path d="M919.7 199.7 L925.0 206.3 L930.3 199.7 L925.0 213.0 Z"></path>
					<g stroke-dasharray="6 6">
							<path d="M144.7 173.0 L87 193 L87 206.33333333333334 L87.0 206.3 " fill="none"></path>
						</g>
					<path d="M81.7 199.7 L87.0 206.3 L92.3 199.7 L87.0 213.0 Z"></path>
					<g stroke-dasharray="6 6">
							<path d="M234.3 173.0 L292 193 L292 206.33333333333334 L292.0 206.3 " fill="none"></path>
						</g>
					<path d="M286.7 199.7 L292.0 206.3 L297.3 199.7 L292.0 213.0 Z"></path>
					<g data-name="All Traffic">
							<g fill="#eee8d5" stroke="#33322E" data-name="All Traffic">
								<rect x="297.5" y="0.0" height="31.0" width="89.0" data-name="All Traffic"></rect>
							</g>
						<g transform="translate(297.5, 0)" font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" data-name="All Traffic">
								<g transform="translate(8, 8)" fill="#33322E" text-align="center" data-name="All Traffic">
									<text x="36.5" y="13.5" stroke="none" text-anchor="middle" data-name="All Traffic">All Traffic</text>
								
								</g>
							</g>
						</g>
					<g data-name="Label = 0">
							<g fill="#eee8d5" stroke="#33322E" data-name="Label = 0">
								<rect x="82.3" y="71.0" height="31.0" width="85.0" data-name="Label = 0"></rect>
							</g>
						<g transform="translate(82.25, 71)" font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" data-name="Label = 0">
								<g transform="translate(8, 8)" fill="#33322E" text-align="center" data-name="Label = 0">
									<text x="34.5" y="13.5" stroke="none" text-anchor="middle" data-name="Label = 0">Label = 0</text>
								
								</g>
							</g>
						</g>
					<g data-name="Label = 1">
							<g fill="#eee8d5" stroke="#33322E" data-name="Label = 1">
								<rect x="608.0" y="71.0" height="31.0" width="85.0" data-name="Label = 1"></rect>
							</g>
						<g transform="translate(608, 71)" font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" data-name="Label = 1">
								<g transform="translate(8, 8)" fill="#33322E" text-align="center" data-name="Label = 1">
									<text x="34.5" y="13.5" stroke="none" text-anchor="middle" data-name="Label = 1">Label = 1</text>
								
								</g>
							</g>
						</g>
					<g data-name="Benign">
							<g fill="#eee8d5" stroke="#33322E" data-name="Benign">
								<rect x="25.0" y="142.0" height="31.0" width="70.0" data-name="Benign"></rect>
							</g>
						<g transform="translate(25, 142)" font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" data-name="Benign">
								<g transform="translate(8, 8)" fill="#33322E" text-align="center" data-name="Benign">
									<text x="27.0" y="13.5" stroke="none" text-anchor="middle" data-name="Benign">Benign</text>
								
								</g>
							</g>
						</g>
					<g data-name="Background">
							<g fill="#eee8d5" stroke="#33322E" data-name="Background">
								<rect x="135.0" y="142.0" height="31.0" width="109.0" data-name="Background"></rect>
							</g>
						<g transform="translate(135, 142)" font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" data-name="Background">
								<g transform="translate(8, 8)" fill="#33322E" text-align="center" data-name="Background">
									<text x="46.5" y="13.5" stroke="none" text-anchor="middle" data-name="Background">Background</text>
								
								</g>
							</g>
						</g>
					<g data-name="Known Malicioous">
							<g fill="#eee8d5" stroke="#33322E" data-name="Known Malicioous">
								<rect x="572.5" y="142.0" height="31.0" width="156.0" data-name="Known Malicioous"></rect>
							</g>
						<g transform="translate(572.5, 142)" font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" data-name="Known Malicioous">
								<g transform="translate(8, 8)" fill="#33322E" text-align="center" data-name="Known Malicioous">
									<text x="70.0" y="13.5" stroke="none" text-anchor="middle" data-name="Known Malicioous">Known Malicioous</text>
								
								</g>
							</g>
						</g>
					<g data-name="Probing">
							<g fill="#eee8d5" stroke="#33322E" data-name="Probing">
								<rect x="410.0" y="213.0" height="31.0" width="76.0" data-name="Probing"></rect>
							</g>
						<g transform="translate(410, 213)" font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" data-name="Probing">
								<g transform="translate(8, 8)" fill="#33322E" text-align="center" data-name="Probing">
									<text x="30.0" y="13.5" stroke="none" text-anchor="middle" data-name="Probing">Probing</text>
								
								</g>
							</g>
						</g>
					<g data-name="Bruteforce">
							<g fill="#eee8d5" stroke="#33322E" data-name="Bruteforce">
								<rect x="526.0" y="213.0" height="31.0" width="97.0" data-name="Bruteforce"></rect>
							</g>
						<g transform="translate(526, 213)" font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" data-name="Bruteforce">
								<g transform="translate(8, 8)" fill="#33322E" text-align="center" data-name="Bruteforce">
									<text x="40.5" y="13.5" stroke="none" text-anchor="middle" data-name="Bruteforce">Bruteforce</text>
								
								</g>
							</g>
						</g>
					<g data-name="Brutefore-XML">
							<g fill="#eee8d5" stroke="#33322E" data-name="Brutefore-XML">
								<rect x="663.0" y="213.0" height="31.0" width="127.0" data-name="Brutefore-XML"></rect>
							</g>
						<g transform="translate(663, 213)" font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" data-name="Brutefore-XML">
								<g transform="translate(8, 8)" fill="#33322E" text-align="center" data-name="Brutefore-XML">
									<text x="55.5" y="13.5" stroke="none" text-anchor="middle" data-name="Brutefore-XML">Brutefore-XML</text>
								
								</g>
							</g>
						</g>
					<g data-name="XMRIGCC CryptoMiner">
							<g fill="#eee8d5" stroke="#33322E" data-name="XMRIGCC CryptoMiner">
								<rect x="830.0" y="213.0" height="31.0" width="190.0" data-name="XMRIGCC CryptoMiner"></rect>
							</g>
						<g transform="translate(830, 213)" font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" data-name="XMRIGCC CryptoMiner">
								<g transform="translate(8, 8)" fill="#33322E" text-align="center" data-name="XMRIGCC CryptoMiner">
									<text x="87.0" y="13.5" stroke="none" text-anchor="middle" data-name="XMRIGCC CryptoMiner">XMRIGCC CryptoMiner</text>
								
								</g>
							</g>
						</g>
					<g data-name="Potentially Malicious">
							<g fill="#eee8d5" stroke="#33322E" data-name="Potentially Malicious">
								<rect x="0.0" y="213.0" height="31.0" width="174.0" data-name="Potentially Malicious"></rect>
							</g>
						<g transform="translate(0, 213)" font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" data-name="Potentially Malicious">
								<g transform="translate(8, 8)" fill="#33322E" text-align="center" data-name="Potentially Malicious">
									<text x="79.0" y="13.5" stroke="none" text-anchor="middle" data-name="Potentially Malicious">Potentially Malicious</text>
								
								</g>
							</g>
						</g>
					<g data-name="Potentially Benign">
							<g fill="#eee8d5" stroke="#33322E" data-name="Potentially Benign">
								<rect x="214.0" y="213.0" height="31.0" width="156.0" data-name="Potentially Benign"></rect>
							</g>
						<g transform="translate(214, 213)" font-family="Helvetica" font-size="12pt" font-weight="bold" font-style="normal" data-name="Potentially Benign">
								<g transform="translate(8, 8)" fill="#33322E" text-align="center" data-name="Potentially Benign">
									<text x="70.0" y="13.5" stroke="none" text-anchor="middle" data-name="Potentially Benign">Potentially Benign</text>
								
								</g>
							</g>
						</g>
					</g>
				</g>
			</g>
		</g>
	</svg>Diagram (1).svg…]()

