import network  # type: ignore ONLY MICROPYTHON
import time
import threading
import sys
from connect import connect_to_wifi
from client import create_socket, start_receiver, send_message
from host import create_access_point, start_host
from server import run_server
import microphone

YAPPER_ID = 4  # Pico order in daisy chain (4 -> 3 -> 2 -> 1)

SSID = f"PicoW_Network{YAPPER_ID}"  # Change to your desired network name
PASSWORD = "12345678"  # Minimum 8 characters
IP_ADDRESS = "192.168.1.0"  # Static IP for the AP (Access Point)
SOCKET_PORT = 8240  # Port for the socket server (same for every Pico)
APS = [
    "PicoW_Network3",
    "PicoW_Network2",
    "PicoW_Network1",
]  # Access points of each pico wifi hotspot

VOLUME_THRESHOLD = 5000  # adjust as needed
SAMPLE_RATE = 2500  # Hz


def monitor_audio():
    adc = microphone.setup_adc(26)
    while True:
        sample = adc.read_u16() - 32768  # center around zero
        if abs(sample) > VOLUME_THRESHOLD:
            print("Loud sound detected, recording snippet...")
            snippet = microphone.record_audio(adc, SAMPLE_RATE, record_time=0.1)
            snippet_bytes = snippet.tobytes()
            try:
                send_message(snippet_bytes, (IP_ADDRESS, SOCKET_PORT))
                print("Snippet sent.")
            except Exception as e:
                print("Error sending snippet:", e)
            time.sleep(0.5)  # pause to avoid flooding
        time.sleep(0.01)  # poll delay


if YAPPER_ID != 1:  # Connect to the next Pico in the chain
    try:
        for i in range(YAPPER_ID):
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

    # Notify the server that the Pico is connected
    send_message(
        f"[+] PICO [{YAPPER_ID}]: Connected.".encode("utf-8"),
        (IP_ADDRESS, SOCKET_PORT),
    )

if YAPPER_ID != 4:  # Create the AP for the previous Pico in the chain
    # Create the AP for the next Pico in the chain
    create_access_point(password=PASSWORD, ssid=SSID, ip_address=IP_ADDRESS)

    # Start the server for the next Pico in the chain
    start_host(ip_address=IP_ADDRESS, yapper_id=YAPPER_ID)

    # Create socket server
    server_thread = threading.Thread(
        target=run_server, args=(IP_ADDRESS, YAPPER_ID), daemon=True
    )
    server_thread.start()

# Start background thread for monitoring audio volume and sending snippet
audio_thread = threading.Thread(target=monitor_audio, daemon=True)
audio_thread.start()
