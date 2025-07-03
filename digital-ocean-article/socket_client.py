import socket

def client_program():
    host = socket.gethostname()  # Get the local machine name
    port = 5000  # The same port as used by the server
    client_socket = socket.socket()  # Create a socket object
    client_socket.connect((host, port))  # Connect to the server

    message = input(" -> ")

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # Send the message to the server
        data = client_socket.recv(1024).decode()
        print(f"Received from server: {data}")
        message = input(" -> ")

    client_socket.close()  # Close the socket when done

if __name__ == '__main__':
    client_program()