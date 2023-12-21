#!/usr/bin/env python3

import os
import subprocess
import sys

# Function to execute shell commands with error handling (12th Dec 2023, cyberoil1997)
def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e}")
        print("This might be due to missing permissions, incorrect command, or package issues.")
        sys.exit(1)

# Install OpenVPN on Raspberry Pi (13th Dec 2023, cyberoil1997)
def install_openvpn():
    print("Installing OpenVPN...")
    run_command('sudo apt-get update')
    run_command('sudo apt-get install -y openvpn')

# Create a basic server config file for OpenVPN (14th Dec 2023, cyberoil1997)
def create_server_config():
    config_content = """
    port 1194
    proto udp
    dev tun
    ca ca.crt
    cert server.crt
    key server.key
    dh dh.pem
    server YOUR_VPN_NETWORK 255.255.255.0
    ifconfig-pool-persist ipp.txt
    push "redirect-gateway def1 bypass-dhcp"
    push "dhcp-option DNS YOUR_DNS"
    keepalive 10 120
    tls-auth ta.key 0
    cipher AES-256-CBC
    persist-key
    persist-tun
    status openvpn-status.log
    verb 3
    """
    try:
        with open("/etc/openvpn/server.conf", "w") as file:
            file.write(config_content)
        print("Server config created. Edit the file to add your network details.")
    except IOError as e:
        print(f"Error writing server config: {e}")
        print("This might be due to permission issues or disk space.")
        sys.exit(1)

# Set up basic client configuration for OpenVPN (16th Dec 2023, cyberoil1997)
def setup_client_config():
    client_config = """
    client
    dev tun
    proto udp
    remote YOUR_SERVER_IP 1194
    resolv-retry infinite
    nobind
    persist-key
    persist-tun
    ca ca.crt
    cert client.crt
    key client.key
    remote-cert-tls server
    tls-auth ta.key 1
    cipher AES-256-CBC
    verb 3
    """
    client_name = input("Enter your client name: ")
    try:
        with open(f"{client_name}.ovpn", "w") as file:
            file.write(client_config)
        print(f"Client config for {client_name} created. Add your server IP and certificates.")
    except IOError as e:
        print(f"Error writing client config: {e}")
        print("This might be due to permission issues or disk space.")
        sys.exit(1)

# Main function for VPN setup (17th Dec 2023, cyberoil1997)
def main():
    install_openvpn()
    create_server_config()
    setup_client_config()

if __name__ == "__main__":
    main() # Script execution begins here (20th Dec 2023, cyberoil1997)
