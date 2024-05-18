from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from Event.EventHandler import EventManager
from Event.UpdateStreamEventHandler import UpdateStreamEventHandler
from Event.UpdateHistoryNewEventHandler import UpdateHistoryNewEventHandler
from Configuration import Configuration


class PoDriver(webdriver.Chrome):
    def __init__(self):
        service = Service(executable_path=Configuration.CHROME_DRIVER_PATH)
        options = Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        webdriver.Chrome.__init__(self, service=service, options=options)