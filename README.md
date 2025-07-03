# Pub-Sub Middleware

A comprehensive implementation of the Publisher-Subscriber pattern using Python and WebSocket technology.

## Overview

This project demonstrates a publish-subscribe messaging pattern implementation where publishers categorize messages into topics and subscribers express interest in one or more topics to receive relevant messages. This decoupled architecture allows for flexible, scalable communication between components.

## Project Structure

- **Demo/**: A web-based demonstration of the pub-sub system
  - Interactive UI for publishing messages and subscribing to topics
  - Real-time updates and visual feedback
  - Built with HTML, CSS, and JavaScript frontend with Python backend

- **Assignment/**: Implementation of specific tasks
  - **Task1/**: Basic client-server socket communication

- **Python/**: Core Python implementation of the pub-sub pattern
  - `pybsub.py`: Python implementation of the publisher-subscriber middleware

- **Digital Ocean Article Examples/**: Socket programming examples
  - Basic socket server and client implementation
  - Based on the Digital Ocean tutorial

- **YouTube Tutorial Implementation/**: 
  - Client-server communication examples
  - Based on the Tech With Tim tutorial

## How It Works

1. **Publishers** send messages to specific topics
2. The **Middleware** maintains the topic registry and manages message distribution
3. **Subscribers** register interest in topics and receive only relevant messages

## Features

- Topic-based message filtering
- Real-time message delivery
- Web-based user interface
- Asynchronous communication
- Multiple subscriber support
- Message queuing

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Web browser (for Demo)

### Running the Demo

1. Navigate to the Demo directory:
   ```
   cd Demo
   ```

2. Start the server:
   ```
   python server.py
   ```

3. Open your browser and visit:
   ```
   http://localhost:5000
   ```

### Basic Usage Example

```python
# Import the pub-sub implementation
from Python.pybsub import PubSub

# Create a pub-sub instance
pubsub = PubSub()

# Subscribe to a topic
pubsub.subscribe("user1", "weather")

# Publish a message to a topic
pubsub.publish("weather", "It's sunny today!")

# Receive messages for a subscriber
messages = pubsub.receive("user1")
```

## Resources Used

- [Digital Ocean Tutorial: Python Socket Programming Server Client](https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client)
- [Tech With Tim YouTube Tutorial: Socket Programming in Python](https://www.youtube.com/watch?v=3QiPPX-KeSc)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.