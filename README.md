# CS4390-RDT-over-UDP
This project aims to implement the Go Back N and Selective Repeat formulations of reliable data transfer over UDP.

This project runs on python 2.7+ and requires the following packages: configparser, socket

To use basic-udp-client and basic-udp-server, you will need to create a udp.conf file in the directory from which you are running them.

This file should look like the following:

\[server\]

ip = \<server id address\>

port = \<server port\>


\[client\]

port = \<client port\>

