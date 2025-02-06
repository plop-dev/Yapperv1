import socket
import threading

HOST, PORT = "127.0.0.1", 8240


def create_socket() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)  # Short timeout for non-blocking checks
    return sock


def listen_for_messages(sock: socket.socket, stop_event: threading.Event) -> None:
    """Thread function: continuously receive messages from the server."""
    while not stop_event.is_set():
        try:
            data = sock.recv(1024)  # Blocking with timeout
            if data:
                print("\nReceived: {}".format(data.decode().strip()))
                print("> ", end="", flush=True)  # re-prompt user input if needed
        except socket.timeout:
            continue  # Timeout reached, check stop_event and continue
        except Exception as e:
            print(f"\nAn error occurred while receiving: {e}")
            break


def start_receiver(
    sock: socket.socket, stop_event: threading.Event
) -> threading.Thread:
    receiver_thread = threading.Thread(
        target=listen_for_messages, args=(sock, stop_event), daemon=True
    )
    receiver_thread.start()
    return receiver_thread


def send_message(sock: socket.socket, message: str, address: tuple[str, int]) -> None:
    """Encode and send a message to the given address with error handling."""
    try:
        data = message.encode("utf-8")
        bytes_sent = sock.sendto(data, address)
        if bytes_sent != len(data):
            raise RuntimeError("Incomplete message sent.")
        print("Sent:     {}".format(message))
    except Exception as e:
        print(f"An error occurred while sending the message: {e}")


def main() -> None:
    sock = create_socket()
    stop_event = threading.Event()
    receiver_thread = start_receiver(sock, stop_event)

    print("Enter messages to send. Press Ctrl+C or type 'q' to quit.")

    try:
        while True:
            message = input("> ").strip()
            if message.lower() == "q":
                break

            try:
                send_message(sock, message, (HOST, PORT))
                print("Sent:     {}".format(message))
            except Exception as e:
                print(f"An error occurred while sending: {e}")

    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        stop_event.set()
        sock.close()
        receiver_thread.join()


if __name__ == "__main__":
    main()
