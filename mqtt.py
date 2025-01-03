import paho.mqtt.client as mqtt
import time
import threading

from user_commands.delete_member_response import on_delete_member_response
from user_commands.edit_member_response import on_edit_member_response
from user_commands.list_active_members_response import on_list_active_members_response
from user_commands.list_all_members_response import on_list_all_members_response
from user_commands.new_member_response import on_new_member_response
from user_commands.register_response import on_register_response
from user_commands.general_commands_response import on_general_commands_response
from util.endpoints import Endpoints
from user_commands.login_response import on_login_response


class MQTTServer:
    def __init__(self):
        self._endpoints = Endpoints()
        # MQTT server config
        # broker here is the mosquito broker running on the pi
        self._broker = "100.100.6.69" #used to be: 192.168.1.75
        self._port = 1883
        self._topic = "weird-stuff"
        # set up MQTT client
        self._client = mqtt.Client()
        self._client.username_pw_set(self._endpoints.MQTT_USERNAME, self._endpoints.MQTT_PASSWORD)
        self._client.on_message = self._on_message
        self._connect()
        # subscribe to the topic I need to listen to
        self._client.subscribe("mqtt_responses_cached")
        # self._client.subscribe("magnetic_lock")
        self._client.subscribe("login_response")
        self._client.subscribe("register_response")
        self._client.subscribe("edit_member_status/response")
        self._client.subscribe("forgot_password_response")
        self._client.subscribe("last_active_person")
        self._client.subscribe("all_members_response")
        self._client.subscribe("add_member_response")
        self._client.subscribe("delete_response")
        self._client.subscribe("lock")
        self._client.subscribe("change_password/response")


    @classmethod
    def _on_message(cls, client, userdata, msg):
        try:
            match msg.topic:
                case "register_response":
                    payload = msg.payload.decode()
                    on_register_response(payload)
                case "add_member_response":
                    payload = msg.payload.decode()
                    on_general_commands_response(payload)
                case "edit_member_response":
                    payload = msg.payload.decode()
                    on_edit_member_response(payload)
                case "delete_response":
                    payload = msg.payload.decode()
                    on_delete_member_response(payload)
                case "all_members_response":
                    payload = msg.payload.decode()
                    on_list_all_members_response(payload)
                case "last_active_person":
                    payload = msg.payload.decode()
                    on_list_active_members_response(payload)
                case "magnetic_lock":
                    payload = msg.payload.decode()
                    print(payload)
                case "login_response":
                    payload = msg.payload.decode()
                    on_login_response(payload)
                case "change_password/response":
                    payload = msg.payload.decode()
                    on_general_commands_response(payload)
                case "edit_member_status/response":
                    payload = msg.payload.decode()
                    on_general_commands_response(payload)
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
        while True:
            continue

    def stop_mqtt(self):
        self._client.loop_stop()
        self._client.disconnect()

    def run(self):
        server_thread = threading.Thread(target=self._run)
        server_thread.start()