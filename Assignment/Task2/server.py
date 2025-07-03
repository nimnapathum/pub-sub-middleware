import sys
import socket
import threading

HEADER = 1
FORMAT = 'utf-8'
SUBSCRIBERS = {}  # Dictionary to store subscriber connections
PUBLISHERS = {}   # Dictionary to store publisher connections

def server_program(port=5000):
    host = socket.gethostbyname(socket.gethostname())
    server_socket = socket.socket()  # Create a socket object
    server_socket.bind((host, port))  # Bind the socket to the host and port
    server_socket.listen(5)  # Listen for incoming connections
    print(f"[SERVER LISTENING] on {host}:{port}\n")
    print("------------------------------------")

    while True:
        conn, addr = server_socket.accept()        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS : {str(threading.active_count() - 1)}]")


def handle_client(conn, address):
    try:
        role = conn.recv(1024).decode(FORMAT)
        print(f"[NEW {role} CONNECTION] {address} connected.")
        
        if role == "SUBSCRIBER":
            SUBSCRIBERS[address] = conn
            print_status()
        elif role == "PUBLISHER":
            PUBLISHERS[address] = conn
            print_status()
        else:
            print(f"[ERROR] Unknown role: {role}")
            conn.close()
            return
              
        connected = True

        while connected:
            try:
                message = conn.recv(1024).decode(FORMAT)
                if not message or message.lower() == 'terminate':
                    connected = False
                    print(f"[DISCONNECT] {address} disconnected.")
                    break

                # If this is a publisher, distribute the message to all subscribers
                if address in PUBLISHERS and message:
                    print(f"[MESSAGE FROM PUBLISHER {address}]: {message}")
                    distribute_messages(message, address)
                    # Send acknowledgment back to publisher
                    conn.send(f"Message '{message}' sent to {len(SUBSCRIBERS)} subscribers".encode(FORMAT))
                
                # If this is a subscriber, they shouldn't be sending messages (except terminate)
                elif address in SUBSCRIBERS and message:
                    conn.send("Subscribers cannot send messages. Only publishers can send messages.".encode(FORMAT))
                    
            except Exception as e:
                print(f"[ERROR] Error receiving message from {address}: {e}")
                connected = False

    except Exception as e:
        print(f"[ERROR] Error handling client {address}: {e}")
    finally:
        # Clean up when client disconnects
        if address in SUBSCRIBERS:
            del SUBSCRIBERS[address]
            print(f"[CLEANUP] Removed subscriber {address}")
        if address in PUBLISHERS:
            del PUBLISHERS[address]
            print(f"[CLEANUP] Removed publisher {address}")
        print_status()
        conn.close()

def distribute_messages(message, publisher_address):
    if not SUBSCRIBERS:
        print("[INFO] No subscribers to send message to")
        return
    
    disconnected_subscribers = []
    
    for subscriber_address, subscriber_conn in SUBSCRIBERS.items():
        try:
            formatted_message = f"[FROM PUBLISHER {publisher_address}]: {message}"
            subscriber_conn.send(formatted_message.encode(FORMAT))
            print(f"[MESSAGE SENT] to subscriber {subscriber_address}")
        except Exception as e:
            print(f"[ERROR] Failed to send message to subscriber {subscriber_address}: {e}")
            disconnected_subscribers.append(subscriber_address)
    
    # Remove disconnected subscribers
    for addr in disconnected_subscribers:
        if addr in SUBSCRIBERS:
            del SUBSCRIBERS[addr]
            print(f"[CLEANUP] Removed disconnected subscriber {addr}")

def print_status():
    print(f"[STATUS] Publishers: {len(PUBLISHERS)}, Subscribers: {len(SUBSCRIBERS)}")
    if PUBLISHERS:
        print(f"[PUBLISHERS] {list(PUBLISHERS.keys())}")
    if SUBSCRIBERS:
        print(f"[SUBSCRIBERS] {list(SUBSCRIBERS.keys())}")


if __name__ == "__main__":
    port = (int(sys.argv[1]) if len(sys.argv) > 1 else 5000)
    server_program(port)
    print(f"[SERVER STARTED] on port {port}")
