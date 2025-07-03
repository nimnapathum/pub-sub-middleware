import socket

def server_program():
    host = socket.gethostname()  # Get the local machine name
    port = 5000  # Reserve a port for your service.
    server_socket = socket.socket()  # Create a socket object
    server_socket.bind((host, port))  # Bind the socket to the host and port
    server_socket.listen(5)  # Listen for incoming connections
    print(f"Server listening on {host}:{port}")

    conn, address = server_socket.accept()  # Accept a connection
    print(f"Connection from: {address}")

    while True:
        data = conn.recv(1024).decode()  # Receive data from the client
        if not data:
            break  # Break the loop if no data is received
        print(f"Received from client: {data}")
        data = input(" -> ")
        conn.send(data.encode())  # Echo the received data back to the client

    conn.close()  # Close the connection

if __name__ == '__main__':
    server_program()