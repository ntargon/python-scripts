# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import socket
import sys


def start_echo_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(1)
    print(f"Echo server is running on port {port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        while True:
            data = client_socket.recv(1024)
            print(f"Received: {data.decode()}")
            if not data:
                break
            client_socket.sendall(data)
        client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tcp-echo-server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    start_echo_server(port)
