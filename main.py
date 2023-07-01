import argparse
import socket
import sys
import time
import os
import termcolor
import scapy.all as scapy
import ipaddress
import requests
import json

from rich.console import Console


console = Console()

# functions
def port_scanner(ip, port):

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        sock.settimeout(1)
        
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            return f"Port {port} is open on {ip}"
        else:
            return f"Port {port} is closed on {ip}"
    
    except socket.error:
        pass
    

# ping a ip with ICMP
def icmp_echo(ip, inf, length):
    
    if inf == True:
        os.system(f"ping {ip} -t")
        
    elif inf == False:
        os.system(f"ping {ip} -n {length}")
        
    else:
        print("Something went wrong, please check your input")
        sys.exit(1)


# ping a ip with TCP
def tcp_ping(ip, port):

    try:
        tcp_pinger = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_pinger.settimeout(1)
        
        result = tcp_pinger.connect_ex((ip, port))
        if result == 0:
            return f"{termcolor.colored(ip, 'blue')} | {termcolor.colored('is up on port', 'green')} | {termcolor.colored(port, 'blue')}"
        else:
            return f"{termcolor.colored(ip, 'blue')} | {termcolor.colored('is down on port', 'red')} | {termcolor.colored(port, 'blue')}"

    except socket.error:
        pass


# scan the network for devices
def scan(ip):
    
    arp_request = scapy.ARP(pdst=ip)
    
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    
    broadcast_arp_request = broadcast/arp_request
    
    answered_list = scapy.srp(broadcast_arp_request, timeout=1, verbose=False)[0]
    result = []
    
    for i in range(0, len(answered_list)):
        client_dict = {"ip": answered_list[i][1].psrc, "mac": answered_list[i][1].hwsrc}
        result.append(client_dict)
    
    return result


# get subnet info
def get_subnet_info(ip):
    
    subnet = ipaddress.ip_network(ip)
    console.print(f"[red]Subnet:[/red] [cyan]{subnet}[/cyan]")
    console.print(f"[red]Netmask:[/red] [cyan]{subnet.netmask}[/cyan]")
    console.print(f"[red]Wildcard:[/red] [cyan]{subnet.hostmask}[/cyan]")
    console.print(f"[red]Network address:[/red] [cyan]{subnet.network_address}[/cyan]")
    console.print(f"[red]Broadcast address:[/red] [cyan]{subnet.broadcast_address}[/cyan]")
    console.print(f"[red]Number of hosts:[/red] [cyan]{subnet.num_addresses}[/cyan]")

    return subnet

# ip to geo
def ip_to_geo(ip):
    
    try:
        req = requests.get(f"http://ip-api.com/json/{ip}")
        req.raise_for_status()
        response = req.json()
        
        if response["status"] == "success":
            
            output = {
                "Status": response["status"],
                "Country": response["country"],
                "Country Code": response["countryCode"],
                "Region": response["region"],
                "Region Name": response["regionName"],
                "City": response["city"],
                "ZIP Code": response["zip"],
                "Latitude": response["lat"],
                "Longitude": response["lon"],
                "Timezone": response["timezone"],
                "ISP": response["isp"],
                "Organization": response["org"],
                "AS": response["as"],
                "Query": response["query"]
            }
            
            return json.dumps(output, indent=4)
        
        else:
            return f"[boldred]Request failed with status: {response['message']}[/boldred]"

    except requests.exceptions.RequestException as e:
        return f"[boldred]An error occurred during the request: {str(e)}[/boldred]"
    

# main function
def main():
    
    parser = argparse.ArgumentParser(prog="networker", description=termcolor.colored("A simple network tool", "blue"), epilog=termcolor.colored("Made by: JustYourAvrg", "blue"))
    
    parser.add_argument("--eg", help="Examples of how to use the program", action="store_true")
    parser.add_argument("--scanner", help="Scan a ip for open ports", action="store_true")
    parser.add_argument("--port", help="The port to use", type=int)
    parser.add_argument("--ip", help="The ip to use", type=str)
    parser.add_argument("--tcp", help="Ping a ip with TCP", action="store_true")
    parser.add_argument("--echo", help="Ping a ip with ICMP", action="store_true")
    parser.add_argument("--length", help="How many times to do a action", type=int)
    parser.add_argument("--inf", help="If the action is infinite or not", action="store_true")
    parser.add_argument("--start", help="Starting port", type=int)
    parser.add_argument("--end", help="Ending port", type=int)
    parser.add_argument("--ns", help="network scanner", action="store_true")
    parser.add_argument("--subnet", help="subnet info", action="store_true")
    parser.add_argument("--geo", help="ip to geo", action="store_true")
    parser.add_argument("--version", help="Show the version", action="version", version="%(prog)s 1.0")

    
    args = parser.parse_args()
    
    if args.scanner:
        if args.start and args.end:
            for port in range(args.start, args.end+1):
                print(port_scanner(args.ip, port))
        else:
            print(port_scanner(args.ip, args.port))
            
    elif args.tcp:
        if args.inf:
            while True:
                print(tcp_ping(args.ip, args.port))
                time.sleep(0.5)
        else:
            print(tcp_ping(args.ip, args.port))
            
    elif args.echo:
        icmp_echo(args.ip, args.inf, args.length)
    
    elif args.eg:
        console.print(f"""
        python networker.py [blue]--eg[/blue] | Shows examples
        python networker.py [blue]--scanner --ip --port[/blue] | Scans an IP for open ports
        python networker.py [blue]--scanner --ip --start --end[/blue] | Scans an IP for open ports in a range
        python networker.py [blue]--tcp --ip --port[/blue] | Pings an IP with TCP
        python networker.py [blue]--tcp --ip --port --inf[/blue] | Pings an IP for an infinite amount of time
        python networker.py [blue]--echo --ip --length[/blue] | Pings an IP with ICMP for a certain amount of time
        python networker.py [blue]--echo --ip --inf[/blue] | Pings an IP with ICMP for an infinite amount of time
        python networker.py [blue]--ns[/blue] | Scans the network for devices
        python networker.py [blue]--subnet[/blue] | Shows subnet info
        python networker.py [blue]--geo[/blue] | Shows geo info """, style="cyan bold on black")
    
    elif args.ns:
        print(scan(socket.gethostbyname(socket.gethostname())))
    
    elif args.subnet:
        get_subnet_info(socket.gethostbyname(socket.gethostname()))
    
    elif args.geo:
        print(ip_to_geo(args.ip))


# run the main function
if __name__ == "__main__":
    main()
