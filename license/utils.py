import psutil
import socket
import platform

def get_active_mac_ip():
    mac_ip_list = []
    
    # Get the OS type (e.g., Windows, Linux, Darwin for macOS)
    os_type = platform.system()

    # Iterate over the network interfaces and collect IP and MAC addresses
    for interface, addrs in psutil.net_if_addrs().items():
        mac_address = None
        ip_address = None
        
        for addr in addrs:
            # Check for MAC address (this will always be the link layer address in most cases)
            if addr.family == socket.AF_LINK or addr.family == psutil.AF_LINK:
                mac_address = addr.address

            # Check for IPv4 address
            if addr.family == socket.AF_INET:  # AF_INET is for IPv4 addresses
                ip_address = addr.address

        # If both MAC and IP are found, add them to the list
        if mac_address and ip_address:
            mac_ip_list.append({
                'mac_address': mac_address,
                'ip_address': ip_address,
                'os_type': os_type  # Include the OS type in the result
            })

    return mac_ip_list
