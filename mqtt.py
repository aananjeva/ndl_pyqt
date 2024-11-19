import paho.mqtt.client as mqtt
import time
import threading

from util.endpoints import Endpoints
from user_commands.login_response import on_login_response

class MQTTServer:
    def __init__(self):
        self._endpoints = Endpoints()
        # MQTT server config
        # broker here is the mosquito broker running on the pi
        self._broker = "192.168.1.75"
        self._port = 1883
        self._topic = "weird-stuff"
        # set up MQTT client
        self._client = mqtt.Client()
        self._client.username_pw_set(self._endpoints.MQTT_USERNAME, self._endpoints.MQTT_PASSWORD)
        self._client.on_message = self._on_message
        self._connect()
        # subscribe to the topic I need to listen to
        self._client.subscribe("mqtt_responses_cached")
        self._client.subscribe("magnetic_lock")

    # TODO: how do I handle it?

    @classmethod
    def _on_message(cls, client, userdata, msg):
        try:
            match msg.topic:
                case "mqtt_responses_cached":
                    payload = msg.payload.decode()
                    if on_login_response(payload):
                        # include logging a.k. program logs
                        pass
                    print(payload)
                case "magnetic_lock":
                    payload = msg.payload.decode()
                    print(payload)
                case _:
                    pass
        except Exception as e:
            raise e

    def _connect(self):
        self._client.connect(self._broker, self._port)

    def _mqtt_loop(self):
        self._client.loop_start()

    def send_message(self, message, topic=None):
        if not topic:
            topic = self._topic
        self._client.publish(topic, message)

    def _run(self):
        self._mqtt_loop()
        try:
            while True:
                time.sleep(0.7)
        except KeyboardInterrupt:
            print("Publisher stopped")
        self._client.loop_stop()
        self._client.disconnect()

    def run(self):
        server_thread = threading.Thread(target=self._run)
        server_thread.start()