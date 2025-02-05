import network  # type: ignore ONLY MICROPYTHON
import time
import threading
import sys
from connect import connect_to_wifi
from socket_client import create_socket, start_receiver, send_message

PICO_ID = 4  # Pico order in daisy chain (4 -> 3 -> 2 -> 1)

SSID = "PicoW_Network1"  # Change to your desired network name
PASSWORD = "12345678"  # Minimum 8 characters
IP_ADDRESS = "192.168.1.0"  # Static IP for the AP (Access Point)
SOCKET_PORT = 8240  # Port for the socket server (same for every Pico)
APS = [
    "PicoW_Network3",
    "PicoW_Network2",
    "PicoW_Network1",
]  # Access points of each pico wifi hotspot

try:
    for i in range(PICO_ID):
        if connect_to_wifi(APS[i], PASSWORD):
            print("[+] Connected to:", APS[i])
            break

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

# Connect to the Pico's Socket Server
sock = create_socket()

# Start the receiver thread
stop_event = threading.Event()
receiver_thread = start_receiver(sock, stop_event)

send_message(
    f"[+] PICO [{PICO_ID}]: Connected.".encode("utf-8"),
    (IP_ADDRESS, SOCKET_PORT),
)
