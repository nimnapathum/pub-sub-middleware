from flask import Flask, request, jsonify
from pubsub import Publisher, Subscriber
from flask import send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

CORS(app , origins="http://localhost:5000")  # Adjust the origin as needed

publisher = Publisher()
subscribers_map = {}  # {name: Subscriber instance}

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    name = data['name']
    topic = data['topic']

    if name not in subscribers_map:
        subscribers_map[name] = Subscriber(name)

    publisher.subscribe(subscribers_map[name], topic)
    return jsonify({"message": f"{name} subscribed to {topic}"}), 200


@app.route('/publish', methods=['POST'])
def publish():
    data = request.json
    topic = data['topic']
    message = data['message']

    publisher.publish(message, topic)
    return jsonify({"message": f"Published '{message}' to {topic}"}), 200


@app.route('/receive/<name>', methods=['GET'])
def receive(name):
    if name in subscribers_map:
        msg = subscribers_map[name].receive()
        return jsonify({"message": msg}), 200
    return jsonify({"error": "Subscriber not found"}), 404

@app.route('/topics', methods=['GET'])
def get_topics():
    return jsonify({"topics": list(publisher.subscribers.keys())}), 200


if __name__ == '__main__':
    app.run(debug=True)
