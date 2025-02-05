import socket
import sys

HOST, PORT = "0.0.0.0", 8240

try:
    # Initialize the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Binding socket to {HOST}:{PORT}...")

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")

    # Set to keep track of client addresses
    clients = set()

    while True:
        try:
            data, client_address = server_socket.recvfrom(
                1024
            )  # Buffer size of 1024 bytes

            # Add client address to our set if it's new
            clients.add(client_address)

            try:
                message = data.decode("utf-8")
            except UnicodeDecodeError:
                print("Received data is not valid UTF-8.")
                continue

            print(f"Received data from {client_address[0]}:")
            print(message + "\n")

            # Broadcast the received message to every other client
            for addr in clients:
                if addr != client_address:
                    server_socket.sendto(data, addr)

        except KeyboardInterrupt:
            print("\nCtrl+C pressed. Shutting down server.")
            break  # Exit the while loop gracefully
        except Exception as e:
            print(f"Error handling message: {e}")

except Exception as e:
    print(f"Server error: {e}")
    sys.exit(1)

finally:
    print("Closing server socket...")
    server_socket.close()
