import paho.mqtt.client as mqtt
import json

class MQTTClient:
    def __init__(self, broker_address):
        self.broker_address = broker_address
        self.client = mqtt.Client()
        self.client.connect(self.broker_address)
        self.client.loop_start()  # Start the loop to process network traffic

    def send_to_topic(self, topic, message):
        self.client.publish(topic, json.dumps(message))

    def response_listener(self, topic, callback):
        self.client.subscribe(topic)
        self.client.message_callback_add(topic, callback)

    def on_message(self, client, userdata, msg):
        print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
        # Process the message as needed

    def start_listening(self):
        self.client.on_message = self.on_message
        self.client.loop_forever()  # Keep listening for messages

