import sys
import socket
import threading

HEADER = 1
FORMAT = 'utf-8'
SUBSCRIBERS = {}  # Dictionary to store subscriber connections {address: (conn, topic)}
PUBLISHERS = {}   # Dictionary to store publisher connections {address: (conn, topic)}

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
        details = conn.recv(1024).decode(FORMAT)
        details = details.split(" ")
        role = details[0]
        topic = details[1]
        print(f"[NEW {role} CONNECTION on {topic}] {address} connected.")
        
        if role == "SUBSCRIBER":
            SUBSCRIBERS[address] = (conn, topic)
            print_status()
        elif role == "PUBLISHER":
            PUBLISHERS[address] = (conn, topic)
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

                # If this is a publisher, distribute the message to subscribers of the same topic
                if address in PUBLISHERS and message:
                    publisher_topic = PUBLISHERS[address][1]
                    print(f"[PUBLISHER {address} - {publisher_topic}]: {message}")
                    distribute_messages(message, address, publisher_topic)
                    # Count subscribers for this specific topic
                    topic_subscribers = sum(1 for addr, (conn, topic) in SUBSCRIBERS.items() if topic == publisher_topic)
                    conn.send(f"{publisher_topic} - Message '{message}' sent to {topic_subscribers} subscribers".encode(FORMAT))
                
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

def distribute_messages(message, publisher_address, publisher_topic):
    # Filter subscribers by topic
    topic_subscribers = {addr: (conn, topic) for addr, (conn, topic) in SUBSCRIBERS.items() if topic == publisher_topic}
    
    if not topic_subscribers:
        print(f"[INFO] No subscribers for topic '{publisher_topic}' to send message to")
        return
    
    disconnected_subscribers = []
    
    for subscriber_address, (subscriber_conn, _) in topic_subscribers.items():
        try:
            formatted_message = f"[FROM PUBLISHER {publisher_address} on {publisher_topic}]: {message}"
            subscriber_conn.send(formatted_message.encode(FORMAT))
            print(f"[MESSAGE SENT] to subscriber {subscriber_address} on topic {publisher_topic}")
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
        for addr, (conn, topic) in PUBLISHERS.items():
            print(f"[PUBLISHER] {addr} on topic '{topic}'")
    if SUBSCRIBERS:
        for addr, (conn, topic) in SUBSCRIBERS.items():
            print(f"[SUBSCRIBER] {addr} on topic '{topic}'")


if __name__ == "__main__":
    port = (int(sys.argv[1]) if len(sys.argv) > 1 else 5000)
    server_program(port)
    print(f"[SERVER STARTED] on port {port}")
