import threading

class Publisher:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, subscriber, topic):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        # Prevent duplicate subscriptions
        if subscriber not in self.subscribers[topic]:
            self.subscribers[topic].append(subscriber)

        # ✅ Add topic to subscriber's topic list
        subscriber.topics.add(topic)

    def publish(self, message, topic):
        if topic in self.subscribers:
            for subscriber in self.subscribers[topic]:
                subscriber.event.set()
                subscriber.message = message

class Subscriber:
    def __init__(self, name):
        self.name = name
        self.event = threading.Event()
        self.message = None
        self.topics = set()

    def receive(self):
        self.event.wait()
        msg = self.message
        self.event.clear()
        return msg


# publisher = Publisher()

# subscriber_1 = Subscriber("Subscriber 1")
# subscriber_2 = Subscriber("Subscriber 2")
# subscriber_3 = Subscriber("Subscriber 3")

# publisher.subscribe(subscriber_1, "sports")
# publisher.subscribe(subscriber_2, "entertainment")
# publisher.subscribe(subscriber_3, "sports")

# publisher.publish("Soccer match result", "sports")
# subscriber_1.receive()