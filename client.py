import socket
import threading

HOST, PORT = "127.0.0.1", 8240

# Create the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Set a short timeout so the receiving thread can periodically check for shutdown
sock.settimeout(1)

# An event to signal the receiver thread to stop
stop_event = threading.Event()


def listen_for_messages():
    """Thread function: continuously receive messages from the server."""
    while not stop_event.is_set():
        try:
            data = sock.recv(1024)  # Blocking with timeout
            if data:
                print("\nReceived: {}".format(data.decode().strip()))
                print("> ", end="", flush=True)  # re-prompt user input if needed
        except socket.timeout:
            continue  # timeout reached, check stop_event and loop again
        except Exception as e:
            print(f"\nAn error occurred while receiving: {e}")
            break


# Start the receiving thread
receiver_thread = threading.Thread(target=listen_for_messages, daemon=True)
receiver_thread.start()

print("Enter messages to send. Press Ctrl+C or type 'q' to quit.")

try:
    while True:
        # Read user input from the console
        message = input("> ").strip()
        if message.lower() == "q":
            break

        # Send the message to the server
        try:
            sock.sendto(message.encode("utf-8"), (HOST, PORT))
            print("Sent:     {}".format(message))
        except Exception as e:
            print(f"An error occurred while sending: {e}")

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    # Signal the receiver thread to exit
    stop_event.set()
    sock.close()
    receiver_thread.join()
