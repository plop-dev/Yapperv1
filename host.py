import network  # type: ignore ONLY MICROPYTHON
import socket
import time

# Configuration settings for the access point
SSID = "PicoW_Network1"  # Change to your desired network name
PASSWORD = "12345678"  # Minimum 8 characters
IP_ADDRESS = "192.168.4.1"  # Static IP for the AP


def create_access_point():
    # Create a network WLAN object in AP mode
    ap = network.WLAN(network.AP_IF)
    ap.active(True)

    # Configure the access point with SSID and password
    ap.config(essid=SSID, password=PASSWORD)

    # Set a static IP address
    ap.ifconfig((IP_ADDRESS, "255.255.255.0", IP_ADDRESS, IP_ADDRESS))

    print(f"Access Point '{SSID}' created with IP: {IP_ADDRESS}")

    # Wait until the AP is active
    while not ap.active():
        time.sleep(1)

    print("Access point is now active.")


def start_server():
    # Create a socket and bind it to the AP's IP and port 80
    addr = socket.getaddrinfo(IP_ADDRESS, 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Web server listening on http://{}:80".format(IP_ADDRESS))

    while True:
        try:
            cl, addr = s.accept()
            print("Client connected from", addr)
            request = cl.recv(1024)
            print("Request:", request)

            # Simple response (basic HTML page)
            response = """\
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head><title>Pico W Access Point</title></head>
<body><h1>Welcome to Pico W!</h1><p>You are connected to the access point.</p></body>
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
