import socket

HOST, PORT = "localhost", 8240

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")

    while True:
        data, client_address = server_socket.recvfrom(1024)  # Buffer size of 1024 bytes
        print(f"{client_address[0]} wrote:")
        print(data.decode())
        server_socket.sendto(data, client_address)
