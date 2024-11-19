from dataclasses import dataclass


@dataclass(frozen=True)
class Endpoints:
    # MQTT
    MQTT_USERNAME = "app"
    MQTT_PASSWORD = "ndl@group3"