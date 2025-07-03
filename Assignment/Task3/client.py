import sys
import socket
import threading

def listen_for_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                print(f"\n{data}")
                print(" -> ", end="", flush=True)
        except:
            break

def client_program(host='localhost', port=5000, role='SUBSCRIBER', topic=''):
    client_socket = socket.socket()  # Create a socket object
    
    try:
        client_socket.connect((host, port))  # Connect to the server
        details = role + " " + topic
        client_socket.send(details.encode())
        #client_socket.send(topic.encode())
        
        print(f"Connected as {role}")
        
        if role == 'SUBSCRIBER':
            print(f"You are a subscriber on topic: {topic}. You will receive messages from publishers.")
            print("Type 'terminate' to disconnect.")
            print("Listening for messages...")
            
            # Start listening for messages in a separate thread
            listener_thread = threading.Thread(target=listen_for_messages, args=(client_socket,))
            listener_thread.daemon = True
            listener_thread.start()
            
            # Keep the client alive and allow termination
            while True:
                message = input(" -> ")
                if message.lower().strip() == 'terminate':
                    client_socket.send(message.encode())
                    break
                elif message.strip():  # If user types something other than terminate
                    print("Subscribers can only listen to messages. Type 'terminate' to exit.")
                    
        elif role == 'PUBLISHER':
            print(f"You are a publisher on topic: {topic}. Your messages will be sent to subscribers of this topic.")
            print("Type 'terminate' to disconnect.")
            
            while True:
                message = input(" -> ")
                if message.lower().strip() == 'terminate':
                    client_socket.send(message.encode())
                    break
                else:
                    client_socket.send(message.encode())  # Send the message to the server
                    try:
                        data = client_socket.recv(1024).decode()
                        print(f"Server response: {data}")
                    except:
                        break
        else:
            print("Invalid role. Use PUBLISHER or SUBSCRIBER")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()  # Close the socket when done

if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    role = sys.argv[3] if len(sys.argv) > 3 else 'SUBSCRIBER'
    
    # Validate topic argument
    if len(sys.argv) < 5:
        print("Usage: python client.py <host> <port> <role> <topic>")
        print("Example: python client.py localhost 5000 SUBSCRIBER sports")
        sys.exit(1)
    
    topic = sys.argv[4]
    client_program(host, port, role, topic)