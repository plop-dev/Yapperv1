import network  # type: ignore ONLY MICROPYTHON
import time

# Replace with your Wi-Fi credentials
SSID = "szymon"
PASSWORD = "steamdeck"


def connect_to_wifi(ssid, password):
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(0.1)
        print("Network config:", wlan.ifconfig())
        return True
    except Exception as e:
        print(f"Error connecting to Wi-Fi: {e}")
        return False


if __name__ == "__main__":
    connect_to_wifi(SSID, PASSWORD)
