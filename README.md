# CS4390-RDT-over-UDP
This project aims to implement the Go Back N and Selective Repeat formulations of reliable data transfer over UDP.

This project runs on python 3.9+ and requires the following packages: configparser, socket, struct

To use rdt_client and rdt_server, you will need to create an rdt.conf file in the directory from which you are running them.

See the run_rdt_client_example.py and run_rdt_server_example.py for examples on how to use these scripts.

This file should look like the following:

\[server\]

ip = \<server id address\>

port = \<server port\>

timeout = \<server timeout\>


\[client\]

port = \<client port\>

send_fail_delay = \<time to wait after failing to send a message\>

max_payload_size = \<maximum payload size\>

corrupt_probability = \<probability to artificially corrupt a file\>


\[global\]

mode = \<SR for selective repeat, or GBN for go back N\>

window_size = \<window size\>


## Running on mininet
1. Ensure you have the following files in your mininet VM
    * rdt_udp_topo.py
    * basic-udp-server.py
    * basic-udp-client.py
    * udp.conf
2. Determine what the IP of h1 is (ex. 10.0.0.1) and set the server ip in udp.conf accordingly
3. Run `sudo python3 rdt_udp_topo.py` from within the VM directory containing the files.
4. The outputs of basic-udp-server.py and basic-udp-client.py will be in r.out and s.out respectively.
