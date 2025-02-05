import network  # type: ignore ONLY MICROPYTHON
import time
import sys
from connect import connect_to_wifi

PICO_ID = 4  # Pico order in daisy chain (4 -> 3 -> 2 -> 1)

SSID = "PicoW_Network1"  # Change to your desired network name
PASSWORD = "12345678"  # Minimum 8 characters
IP_ADDRESS = "192.168.4.1"  # Static IP for the AP (Access Point)
APS = [
    "PicoW_Network1",
    "PicoW_Network2",
    "PicoW_Network3",
    "PicoW_Network4",
]  # Access points of each pico wifi hotstop

try:
    for i in range(PICO_ID):
        if connect_to_wifi(APS[i], PASSWORD):
            break

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
