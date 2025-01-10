import sys
import mqtt as mqtt
from daemon.lock_daemon import LockDaemon
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from UserCommands import UserCommands

from mqtt import MQTTServer
from gui import GuiBackend

class SmartLockSystem:
    BROKER_ADDRESS = "localhost"  # Change this to your broker address
    LOGIN_TOPIC = "smartlock/login"
    REGISTER_TOPIC = "smartlock/register"
    STATUS_TOPIC = "smartlock/status"

    def __init__(self):
        self.client = mqtt.MQTTServer()
        self.client.run()
        self.user_commands = UserCommands(self.client)


if __name__ == "__main__":
    # Create the QApplication instance
    # Initialize the MQTT server
    mqtt_server = MQTTServer()
    mqtt_server.run()  # Start the MQTT server
    # Initialize UserCommands with the MQTT server
    gui = GuiBackend(mqtt_server)
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    engine.rootContext().setContextProperty("python", gui)
    # Expose `MyWidget` to QML
    engine.loadFromModule("Main", "Main")
    # engine.load("/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/Main/Main.qml")
    thread_daemon = LockDaemon(mqtt_server)
    thread_daemon.run()
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)


