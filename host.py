import network  # type: ignore ONLY MICROPYTHON
import socket
import time

# Configuration settings for the access point
SSID = "PicoW_Network1"  # Change to your desired network name
PASSWORD = "12345678"  # Minimum 8 characters
IP_ADDRESS = "192.168.4.1"  # Static IP for the AP


def create_access_point(
    password: str = PASSWORD, ssid: str = SSID, ip_address: str = IP_ADDRESS
) -> None:
    # Create a network WLAN object in AP mode
    ap = network.WLAN(network.AP_IF)
    ap.active(True)

    # Configure the access point with SSID and password
    ap.config(essid=ssid, password=password)

    # Set a static IP address
    ap.ifconfig((ip_address, "255.255.255.0", ip_address, ip_address))

    print(f"Access Point '{ssid}' created with IP: {ip_address}")

    # Wait until the AP is active
    while not ap.active():
        time.sleep(1)

    print("Access point is now active.")


def start_server(ip_address: str = IP_ADDRESS, yapper_id: int = 1) -> None:
    # Create a socket and bind it to the AP's IP and port 80
    addr = socket.getaddrinfo(ip_address, 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Web server listening on http://{}:80".format(ip_address))

    while True:
        try:
            cl, addr = s.accept()
            print("Client connected from", addr)
            request = cl.recv(1024)
            print("Request:", request)

            # Simple response (basic HTML page)
            response = f"""\ 
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head><title>Pico W Access Point</title></head>
<body><h1>Welcome to Pico W!</h1><p>You are connected to the access point of PICO {yapper_id}.</p></body>
</html>
"""
            cl.send(response)
            cl.close()
        except Exception as e:
            print("Error:", e)
            cl.close()


# Main script
try:
    create_access_point()
    start_server()
except KeyboardInterrupt:
    print("Program stopped.")
