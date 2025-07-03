import sys
import socket


def server_program(port=5000):
    host = socket.gethostbyname(socket.gethostname())  
    server_socket = socket.socket()  # Create a socket object
    server_socket.bind((host, port))  # Bind the socket to the host and port
    server_socket.listen(5)  # Listen for incoming connections
    print(f"[SERVER LISTENING] on {host}:{port}")
    conn, address = server_socket.accept()  # Accept a connection
    print(f"[NEW CONNECTION] : {address}")

    while True:
        data = conn.recv(1024).decode()  # Receive data from the client
        if not data:
            break  # Break the loop if no data is received
        print(f"[RECEIVED FROM CLIENT] : {data}")
        data = input(" -> ")
        conn.send(data.encode())  # Echo the received data back to the client

    conn.close()  # Close the connection

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    server_program(port)