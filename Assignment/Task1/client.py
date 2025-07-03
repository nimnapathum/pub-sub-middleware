import sys
import socket

def client_program(host='localhost', port=5000):
    client_socket = socket.socket()  # Create a socket object
    client_socket.connect((host, port))  # Connect to the server

    message = input(" -> ")  # Take input from the user

    while message.lower().strip() != 'terminate':
        client_socket.send(message.encode())  # Send the message to the server
        data = client_socket.recv(1024).decode()  # Receive response from the server
        print(f"[RECEIVED FROM SERVER] : {data}")
        message = input(" -> ")  # Take new input

    client_socket.close()  # Close the socket when done

if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    client_program(host, port)