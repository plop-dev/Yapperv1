import socket
import sys

HOST, PORT = "0.0.0.0", 8240


def create_server_socket(host: str, port: int) -> socket.socket:
    """Initialize and bind the UDP server socket."""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(f"Binding socket to {host}:{port}...")
        server_socket.bind((host, port))
        print(f"UDP server listening on {host}:{port}")
        return server_socket
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)


def handle_client_data(
    server_socket: socket.socket, clients: set[tuple[str, int]]
) -> None:
    """Receive, decode, and broadcast messages to clients."""
    try:
        data, client_address = server_socket.recvfrom(1024)
        clients.add(client_address)
        try:
            message = data.decode("utf-8")
        except UnicodeDecodeError:
            print("Received data is not valid UTF-8.")
            return

        print(f"Received data from {client_address[0]}:")
        print(message + "\n")

        # Broadcast the message to every other client
        for addr in clients:
            if addr != client_address:
                server_socket.sendto(data, addr)
    except Exception as e:
        print(f"Error handling message: {e}")


def run_server(host: str, port: int) -> None:
    """Run the main UDP server loop."""
    server_socket = create_server_socket(host, port)
    clients: set[tuple[str, int]] = set()

    try:
        while True:
            handle_client_data(server_socket, clients)
    except KeyboardInterrupt:
        print("\nCtrl+C pressed. Shutting down server.")
    finally:
        print("Closing server socket...")
        server_socket.close()


def main() -> None:
    run_server(HOST, PORT)


if __name__ == "__main__":
    main()
