import socket
import sys
from datetime import datetime

print("""

SIMPLE PYTHON PORTSCANNER BY ROUGEKLAIRE

MENU:

- TO SCAN A CERTAIN WEBSITE TYPE: w
- TO SCAN A CERTAIN IP ADDRESS TYPE: i

type any other letter to exit the program
""")

# capture user input to determine what kind of target should be scanned
what_to_scan = input("Do you want to scan a website (w) or an IP address (i)?:  ")

if what_to_scan.lower() == "w":
    scanned = input("Please enter the website domain: ")
    ip = socket.gethostbyname(scanned)

elif what_to_scan.lower() == "i":
    ip = input("Please enter the IPv4 address: ")

else:
    print("no valid mode selection, please restart the program")
    sys.exit()

# set up basic variables in order to be able to later on give more detailed information about scanned port count or closed and open ports
closed_ports_count = 0
open_ports = []

# print mode selection menu
print("""
MODE SELECTION MENU:

- TO SCAN A RANGE OF PORTS TYPE: a
- TO SCAN A SPECIFIC PORT TYPE: s
""")
mode = input("PLEASE CHOOSE YOUR MODE: ")

# set up custom scanning range
if mode.lower() == "a":
    print("Selected mode: SCAN PORT RANGE \n")
    port_range_start = int(input("Please enter starting port number: "))
    port_range_end = int(input("Please enter ending port number (NOTE: this number is not included): "))

elif mode.lower() == "s":
    print("Selected mode: SCAN SPECIFIC PORT \n")
    port_range_start = int(input("Please enter the port number you want to scan: "))
    port_range_end = port_range_start + 1 # add 1 to the selected port number as the last number in the specified range is not included by default

else:
    print("no valid mode selection, please restart the program")
    sys.exit() # exit the program if no valid mode selection occurred

# information about portscan start
print("\n --- starting portscan --- \n")
starting_time = datetime.now()

try:
    for i in range(port_range_start, port_range_end):
        net_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create basic IPv4 socket object using TCP
        scan = net_sock.connect_ex((ip, i)) # create connection variable which tries to connect to above catched IP-Address for each port within the specified range
        if scan == 0: # check if connection attempt produced exit code 0 i.e. the connection attempt was successful
            print(f"\n [+][+][+]Port {i} is open[+][+][+] \n") # instantly prints out every successful connection attempt including the respective port number
            open_ports.append(i) # append each open port number to the open_ports list in order to be able to display a summary later on
        else:
            print(f"Scanning port {i}: closed") # if connection attemptwas unsuccessful the currently scanned port number is printed in order to see which port is currently scanned
            closed_ports_count += 1 # then the closed port count is increased by 1 in order to be able to later on provide a detailed count of how many ports were closed within the specified range
        net_sock.close() # after determining whether the port is open or closed, each connection within the range is closed
except Exception: # in case something goes wrong an error message is printed and the program closed
    print("[!][!][!]AN ERROR OCCURRED[!][!][!]")
    print("The program is now closing")
    sys.exit()

# creating time and count variables for final information display
ending_time = datetime.now()
scanned_ports = port_range_end - port_range_start
time = ending_time - starting_time

# print out the gathered information
print(f"\n scanned {scanned_ports} port(s) in {time} \n")
print(f"\n scanned {closed_ports_count} closed port(s) \n")
if open_ports != []:
    print("Open ports have been found on port(s):")
    print(*open_ports, sep = "\n")
    print("portscan finished")
else:
    print("\n no open ports have been found \n ")
    print("portscan finished")
