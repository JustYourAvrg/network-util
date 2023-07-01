# network-util
Simple python networking CLI

I will try to update this as my knowledge of python and networking grows

# Utility
- Port Scanner | Scan for open ports on a designated IP Address
- ICMP Pinger | Pings a designated IP Address
- TCP Pinger | Pings a designated IP Address on a specific port
- Network Scanner | Scans for devices connected to the network
- Subnet Info | Gets subnet information 
- IP To Geo | Gets the geolocation of a designated IP Address


# How To Use
## Important
- **You must have python installed 3.9 or higher**
- **You must have pip installed**

## Installation
- **To install the required packages type "pip install -r requirements.txt"**

## Usage
- Port Scanner | To use the port scanner type "python main.py --scanner --ip IPHERE --port PORTHERE" and that will scan a designated port on a certain IP
- Port Scanner | Your can also use "python main.py --scanner --ip IPHERE --start STARTPORT --end ENDPORT" to scan a range of ports on a certain IP
- ICMP Pinger | To use the ICMP Pinger type "python main.py --echo --ip IPHERE --inf" and that will ping a designated IP for an infinite amount of time
- ICMP Pinger | You can also use "python main.py --echo --ip IPHERE --length COUNTHERE" to ping a designated IP a certain amount of times
- TCP Pinger | To use the TCP Pinger type "python main.py --tcp --ip IPHERE --port PORTHERE --inf" and that will ping a designated IP on a certain port for an infinite amount of time
- TCP Pinger | You can also use "python main.py --tcp --ip IPHERE --port PORTHERE" to ping a designated IP on a certain port once
- Network Scanner | To use the Network Scanner type "python main.py --ns" and that will scan the network for devices
- Subnet Info | To use the Subnet Info type "python main.py --subnet" and that will get the subnet information
- IP To Geo | To use the IP To Geo type "python main.py --geo --ip IPHERE" and that will get the geolocation of a designated IP Address
- Examples | To see examples type "python main.py --eg" and that will show you examples of how to use the commands
- Help | To get help type "python main.py --help or -h" and that will show you all the commands and how to use them
