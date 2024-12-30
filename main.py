import sys
import mqtt as mqtt
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
    # trying to run the app
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
    if not engine.rootObjects():
        sys.exit(-1)
    exit_code = app.exec()
    del engine
    sys.exit(exit_code)


    # ---------------------------------------------------------------------------------------------------

    #test for login
    # mqtt = MQTTServer()
    # mqtt.run()
    # user_data = {"username":"root", "password":"1a6719fc847f299114cc00a430549c272fa8cab7aa8ae3e55d9c6f84c62ba102"}
    # mqtt.send_message(json.dumps(user_data), "login")

    # ---------------------------------------------------------------------------------------------------

    # #test for file transfer
    # file_tr = FileTransfer(name="test", surname="test2", file_path="/Users/anastasiaananyeva/Downloads/pics/austin-curtis-YVY61lIO_gw-unsplash.jpg")
    # value = file_tr.file_transfer()
    # if value:
    #     print(value)




