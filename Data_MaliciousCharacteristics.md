# Bruteforce Attack

A Bruteforce (BF) attack is a usefull starting place for this project. For piece of hardware where a each login attempt is made, a corresponding connection must be established and authentication also attempted. Because of this, if the authentication is unsucessfull, then the program must continue down its configured dictionary attack.

We can infer that attacks of this sort will display a suspiciously large volume of SYN & RST flags.

SYN flags (Flow_SYN_flag_count): SYN stands for "Synchronize." It's used to initiate a connection. The count of SYN flags in a flow would indicate how many times a connection was initiated. A clear indication of a scan occurrence would be when the high volume identified corresponds to a particular destination machine with the destination port varience being high and th source port remaining constant.

RST flags (Flow_RST_flag_count): RST stands for "Reset." It is used to reset a connection. The count of RST flags in a flow would indicate how many times a connection was forcefully terminated or reset.

With some context we can also assume that the high counts for SYN and RST flags would most likely be proceeded by some ICMP requests.
