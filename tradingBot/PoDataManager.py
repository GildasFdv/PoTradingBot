from threading import Thread
from enum import IntEnum
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from Event.EventHandler import EventManager
from Event.UpdateStreamEventHandler import UpdateStreamEventHandler
from Event.UpdateHistoryNewEventHandler import UpdateHistoryNewEventHandler
import json
import base64
from Configuration import Configuration
from threading import Lock
from Event.PoCandle import Candle, CandleIndex
from PoDriver import PoDriver

class PoDataManagerParams(IntEnum):
    PO_DRIVER = 0
    CANDLES_LOCK = 1
    CANDLES = 2

class PoDataManager(Thread):

    def __init__(self, args):
        Thread.__init__(self, args=args, name='PoDataManager')
        self.running = True

        self.candles_lock = args[PoDataManagerParams.CANDLES_LOCK]
        self.candles_lock.acquire()
        self.candles = args[PoDataManagerParams.CANDLES]
        self.candles_lock.release()

        self.driver = args[PoDataManagerParams.PO_DRIVER]

        self.eventManager = EventManager()
        self.eventManager.registerEventHandler('updateHistoryNew', UpdateHistoryNewEventHandler())
        self.eventManager.registerEventHandler('updateStream', UpdateStreamEventHandler())


    def run(self):
        print("Data Manager: started")

        while self.running:
            for wsData in self.driver.get_log('performance'):

                if '"opcode":1' in wsData['message']:
                    try: 
                        message = json.loads(wsData['message'])['message']
                        response = message.get('params', {}).get('response', {})
                        payload = response['payloadData']
                        json_part = payload.split('-', 1)[1]
                        parsed_json = json.loads(json_part)
                        event_name = parsed_json[0]
                        self.eventManager.setEventReceived(event_name)
                    finally:
                        continue

                if self.eventManager.isEventReceived():
                    message = json.loads(wsData['message'])['message']
                    response = message.get('params', {}).get('response', {})
                    if 'payloadData' in response:
                        payload = base64.b64decode(response['payloadData']).decode('utf-8')
                        data = json.loads(payload)
                        self.candles_lock.acquire()
                        self.eventManager.handleEvent(data, self.candles)
                        self.candles_lock.release()

        self.driver.quit()

    def stop(self):
        self.running = False
        print("Data Manager: stopped")