# CS4390-RDT-over-UDP

### Summary:
This project aims to implement the Go Back N and Selective Repeat formulations of reliable data transfer over UDP.

### Requirements:
This project runs on python 3.9+ and requires the following packages: configparser, socket, recordclass

### How to run:
To run the tests, cd into `./validation-relay/` and run `python3 validation-relay.py`,
this will run all tests by setting up a relay server which will emulate the delay and loss of a network.
In order to run a specific test, comment out all non-relevant tests in the `__main__` of validation-relay.py.

### Project structure:
```
.
|-- gbn # our GBN implimentation
|   |-- gbn_client.py # our GBN client class
|   |-- gbn_server.py # our GBN server class
|   `-- __init__.py
|-- rdt # our RDT implimentation
|   |-- __init__.py
|   |-- myfile.txt # short test text file
|   |-- rdt_client.py
|   |-- rdt.conf # configuration for examples
|   |-- rdt_headers.py
|   |-- rdt_server.py
|   |-- record_definitions.py
|   |-- run_rdt_client_example.py
|   |-- run_rdt_server_example.py
|   `-- send_packet.py
|-- README.md # this file
|-- relay_example
|   `-- basic_udp
|       |-- basic-udp-client.py
|       |-- basic-udp-server.py
|       |-- rdt_udp_topo.py
|       |-- relay.conf
|       `-- testFile.txt # short test text file
|-- requirements.txt
|-- sr # our SR implimentation
|   |-- __init__.py
|   |-- sr_client.py # our SR client class
|   `-- sr_server.py # our SR server class
>-- validation-mininet # non-functional validation suite utilizing mininet, safe to ignore. use validation-relay instead
`-- validation-relay # our validation suite using a relay server which emulates a network
    |-- 500K.txt # file for running validation tests
    |-- cmd_launcher.py # command line interface for launching GBN/SR servers/clients with a given configuration
    |-- relay.py # command line interface to launch relay server 
    `-- validation-relay.py # main validation file
```