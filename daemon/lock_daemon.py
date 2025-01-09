from threading import Thread
from time import sleep

from gui import GuiBackend
from mqtt import MQTTServer
from loguru import logger


class LockDaemon:
    def __init__(self, mqtt: MQTTServer):
        self._gui = GuiBackend(mqtt)

    def get_status(self):
        try:
            with open("/Users/anastasiaananyeva/PycharmProjects/ndl_pyqt/mqtt_responses_cached/magnetic_lock_authorized.csv", "r") as file:
                content = file.read().lower()
            if not content:
                raise Exception("No magnetic lock status found")

            if content == "open":
                self._gui.lock_status_manual("open")
            else:
                self._gui.lock_status_manual("close")

        except Exception as e:
            logger.exception(e)


    def _run(self):
        try:
            while True:
                logger.debug("I am running")
                self.get_status()
                logger.debug("I am done")
                sleep(30)
        except Exception as e:
            logger.critical(e)

    def run(self):
        thread = Thread(target=self._run)
        thread.start()

