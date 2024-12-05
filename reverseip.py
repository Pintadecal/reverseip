# -*- coding: Latin-1 -*-
import os
import sys
from requests import get
from colorama import Fore, Style, init
from fake_headers import Headers
from re import findall
from multiprocessing.dummy import Pool
import ctypes

# Clear the console screen
os.system('cls' if os.name == 'nt' else 'clear')

# Set the console title on Windows
if os.name == 'nt':
    ctypes.windll.kernel32.SetConsoleTitleW('PINTADECAL REVERSE IP LOOKUP')
else:
    sys.stdout.write('PINTADECAL IP LOOKUP\n')

# Initialize colorama for automatic reset after each print
init(autoreset=True)

# Define color variables
RED = Fore.RED
GREEN = Fore.GREEN
WHITE = Fore.WHITE
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
BRIGHT_GREEN = Fore.LIGHTGREEN_EX
BRIGHT_CYAN = Fore.LIGHTCYAN_EX

# Generate fake browser headers to mimic Chrome on Windows
header = Headers(browser='chrome', os='win', headers=True)

# Set to keep track of processed domains
processed_domains = set()

# Function to process each IP address
def process_ip(ip):
    fetch_domains_from_ip(ip)

# Function to fetch domains associated with an IP
def fetch_domains_from_ip(ip):
    try:
        # Query the website with the provided IP
        url = f'https://ipchaxun.com/{ip}/'
        response = get(url, timeout=10).text
        
        # Extract domains from the HTML response
        domains = findall(r'www\.[a-zA-Z0-9-]+\.[a-zA-Z.]+', response)
        
        # Save and display the found domains
        save_domains(ip, domains, '[ PINTADECAL REVERSE IP ] ==> ')
    except Exception as e:
        print(f"{RED}[Error]{WHITE} Failed to fetch domains for IP: {YELLOW}{ip}")

# Function to filter, save, and display domains
def save_domains(ip, domains, label):
    new_domains = []
    
    for domain in domains:
        # Clean up domain names by removing unwanted parts
        domain = domain.lower().replace("www.", "").replace("<td>", "").replace("</td>", "")
        
        # Skip common subdomains
        if not any(domain.startswith(prefix) for prefix in ["webmail.", "ftp.", "cpanel.", "webdisk.", "cpcalendars.", "mail.", "cpcontacts.", "ns1.", "ns2."]):
            # Add new domain to the processed set
            if domain not in processed_domains:
                processed_domains.add(domain)
                new_domains.append(domain)
                
                # Display the domain along with the IP
                print(f'{RED}{label}{YELLOW} [Domain Found] {GREEN}{ip} {YELLOW}>> {WHITE}{domain}')
    
    # If new domains are found, save them to the file
    if new_domains:
        with open('Grabbed.txt', 'a') as file:
            file.write("\n".join(new_domains) + '\n')

# Main function for user interaction and IP processing
def main():
    BANNER = f"""{RED}
  _____                                _____ _____  
 |  __ \                              |_   _|  __ \ 
 | |__) |_____   _____ _ __ ___  ___    | | | |__) |
 |  _  // _ \ \ / / _ \ '__/ __|/ _ \   | | |  ___/ 
 | | \ \  __/\ V /  __/ |  \__ \  __/  _| |_| |     
 |_|  \_\___| \_/ \___|_|  |___/\___| |_____|_|     
                                                    
             {GREEN} coded by Pintadecal <3 
    """
    print(BANNER)

    # Ask the user for the IP list file and the number of threads
    ip_list_file = input(f'{RED}Enter the IP list file: {WHITE}')
    pool_amount = int(input(f"{RED}Number of threads: {WHITE}"))
    
    # Read IP addresses from the file
    with open(ip_list_file, mode='r', errors='ignore') as file:
        ips = file.read().splitlines()
    
    # Use a thread pool to process the IP addresses concurrently
    with Pool(pool_amount) as pool:
        pool.map(process_ip, ips)

    # Wait for user input before closing
    input(f"{BRIGHT_GREEN}Press any key to exit...")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
