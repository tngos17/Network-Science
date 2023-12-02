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

# A First Glance - Data Features (HIKARI-2021)
Here are the features Implemented by the dataset. To better understand and appreciate their selection I highly recommend reading the full publication.

| No  | Feature                        | Description                                         |
|----|--------------------------------|-----------------------------------------------------|
| 1  | uid                            | Unique identifier for each record.                   |
| 2  | originh                        | Source host of the network flow.                     |
| 3  | originp                        | Source port of the network flow.                     |
| 4  | responh                         | Destination host of the network flow.                |
| 5  | responp                         | Destination port of the network flow.                |
| 6  | flow_duration                   | Duration of the network flow.                        |
| 7  | fwd_pkts_tot                    | Total number of forward packets in the flow.        |
| 8  | bwd_pkts_tot                    | Total number of backward packets in the flow.       |
| 9  | fwd_data_pkts_tot               | Total number of forward data packets in the flow.   |
| 10 | bwd_data_pkts_tot               | Total number of backward data packets in the flow.  |
| 11 | fwd_pkts_per_sec                | Packets per second for forward flow.                 |
| 12 | bwd_pkts_per_sec                | Packets per second for backward flow.                |
| 13 | flow_pkts_per_sec                | Packets per second for the entire flow.              |
| 14 | down_up_ratio                   | Ratio of downstream to upstream traffic.            |
| 15 | fwd_header_size_tot             | Total header size for forward flow.                 |
| 16 | fwd_header_size_min             | Minimum header size for forward flow.               |
| 17 | fwd_header_size_max             | Maximum header size for forward flow.               |
| 18 | bwd_header_size_tot             | Total header size for backward flow.                |
| 19 | bwd_header_size_min             | Minimum header size for backward flow.              |
| 20 | bwd_header_size_max             | Maximum header size for backward flow.              |
| 21 | flow_FIN_flag_count             | Count of FIN flags in the flow.                     |
| 22 | flow_SYN_flag_count             | Count of SYN flags in the flow.                     |
| 23 | flow_RST_flag_count             | Count of RST flags in the flow.                     |
| 24 | fwd_PSH_flag_count              | Count of PSH flags in the forward flow.             |
| 25 | bwd_PSH_flag_count              | Count of PSH flags in the backward flow.            |
| 26 | flow_ACK_flag_count              | Count of ACK flags in the flow.                     |
| 27 | fwd_URG_flag_count              | Count of URG flags in the forward flow.             |
| 28 | bwd_URG_flag_count              | Count of URG flags in the backward flow.            |
| 29 | flow_CWR_flag_count              | Count of CWR flags in the flow.                     |
| 30 | flow_ECE_flag_count              | Count of ECE flags in the flow.                     |
| 31 | fwd_pkts_payload.min            | Minimum payload size for forward packets.           |
| 32 | fwd_pkts_payload.max            | Maximum payload size for forward packets.           |
| 33 | fwd_pkts_payload.tot            | Total payload size for forward packets.             |
| 34 | fwd_pkts_payload.avg            | Average payload size for forward packets.           |
| 35 | fwd_pkts_payload.std            | Standard deviation of payload size for forward packets.|
| 36 | bwd_pkts_payload.min            | Minimum payload size for backward packets.          |
| 37 | bwd_pkts_payload.max            | Maximum payload size for backward packets.          |
| 38 | bwd_pkts_payload.tot            | Total payload size for backward packets.            |
| 39 | bwd_pkts_payload.avg            | Average payload size for backward packets.          |
| 40 | bwd_pkts_payload.std            | Standard deviation of payload size for backward packets.|
| 41 | flow_pkts_payload.min           | Minimum payload size for the entire flow.           |
| 42 | flow_pkts_payload.max           | Maximum payload size for the entire flow.           |
| 43 | flow_pkts_payload.tot           | Total payload size for the entire flow.             |
| 44 | flow_pkts_payload.avg           | Average payload size for the entire flow.           |
| 45 | flow_pkts_payload.std           | Standard deviation of payload size for the entire flow.|
| 46 | fwd_iat.min                     | Minimum inter-arrival time for forward flow.        |
| 47 | fwd_iat.max                     | Maximum inter-arrival time for forward flow.        |
| 48 | fwd_iat.tot                     | Total inter-arrival time for forward flow.          |
| 49 | fwd_iat.avg                     | Average inter-arrival time for forward flow.        |
| 50 | fwd_iat.std                     | Standard deviation of inter-arrival time for forward flow.|
| 51 | bwd_iat.min                     | Minimum inter-arrival time for backward flow.       |
| 52 | bwd_iat.max                     | Maximum inter-arrival time for backward flow.       |
| 53 | bwd_iat.tot                     | Total inter-arrival time for backward flow.         |
| 54 | bwd_iat.avg                     | Average inter-arrival time for backward flow.       |
| 55 | bwd_iat.std                     | Standard deviation of inter-arrival time for backward flow.|
| 56 | flow_iat.min                    | Minimum inter-arrival time for the entire flow.     |
| 57 | flow_iat.max                    | Maximum inter-arrival time for the entire flow.     |
| 58 | flow_iat.tot                    | Total inter-arrival time for the entire flow.       |
| 59 | flow_iat.avg                    | Average inter-arrival time for the entire flow.     |
| 60 | flow_iat.std                    | Standard deviation of inter-arrival time for the entire flow.|
| 61 | payload_bytes_per_second        | Payload transfer rate in bytes per second.          |
| 62 | fwd_subflow_pkts                | Number of packets in the forward subflow.          |
| 63 | bwd_subflow_pkts                | Number of packets in the backward subflow.         |
| 64 | fwd_subflow_bytes               | Number of bytes in the forward subflow.            |
| 65 | bwd_subflow_bytes               | Number of bytes in the backward subflow.           |
| 66 | fwd_bulk_bytes                  | Total bulk bytes for the forward flow.             |
| 67 | bwd_bulk_bytes                  | Total bulk bytes for the backward flow.            |
| 68 | fwd_bulk_packets                | Total bulk packets for the forward flow.           |
| 69 | bwd_bulk_packets                | Total bulk packets for the backward flow.          |
| 70 | fwd_bulk_rate                   | Bulk transfer rate for the forward flow.           |
| 71 | bwd_bulk_rate                   | Bulk transfer rate for the backward flow.          |
| 72 | active.min                      | Minimum active time.                               |
| 73 | active.max                      | Maximum active time.                               |
| 74 | active.tot                      | Total active time.                                 |
| 75 | active.avg                      | Average active time.                               |
| 76 | active.std                      | Standard deviation of active time.                 |
| 77 | idle.min                        | Minimum idle time.                                 |
| 78 | idle.max                        | Maximum idle time.                                 |
| 79 | idle.tot                        | Total idle time.                                   |
| 80 | idle.avg                        | Average idle time.                                 |
| 81 | idle.std                        | Standard deviation of idle time.                   |
| 82 | fwd_init_window_size            | Initial window size for the forward flow.         |
| 83 | bwd_init_window_size            | Initial window size for the backward flow.        |
| 84 | fwd_last_window_size            | Last window size for the forward flow.            |
| 85 | traffic_category                | Category of network traffic.                       |
| 86 | Label                           | The label assigned to the network flow, possibly indicating normal or malicious activity.|
