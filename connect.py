# Wifi Connection

import network  # type: ignore MICROPYTHON ONLY
import time

# Replace with your Wi-Fi credentials

SSID = "szymon"
PASSWORD = "steamdeck"

# Initialize the Wi-Fi interface

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to the Wi-Fi network

print("Connecting to network...")
wlan.connect(SSID, PASSWORD)

# Wait for the connection to establish

timeout = 10  # seconds
start_time = time.time()

while not wlan.isconnected():
    if time.time() - start_time > timeout:
        print("Connection timed out")
        break
    print("Waiting for connection...")
    time.sleep(1)

# Check if connected

if wlan.isconnected():
    print("Connected to Wi-Fi!")
    print("Network config:", wlan.ifconfig())
else:
    print("Failed to connect to Wi-Fi.")
