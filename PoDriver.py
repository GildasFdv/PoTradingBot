from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from Event.EventHandler import EventManager
from Event.UpdateStreamEventHandler import UpdateStreamEventHandler
from Event.UpdateHistoryNewEventHandler import UpdateHistoryNewEventHandler
from Configuration import Configuration
from time import sleep
import pickle


class PoDriver(webdriver.Chrome):
    def __init__(self):
        service = Service(executable_path=Configuration.CHROME_DRIVER_PATH)
        options = Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        webdriver.Chrome.__init__(self, service=service, options=options)

        try:
            self.get(Configuration.URL)
            self.load_cookies(Configuration.COOKIES_FILE)
            self.get(Configuration.URL)
        except FileNotFoundError:
            self.get(Configuration.URL)
            sleep(10)
            self.save_cookies(Configuration.COOKIES_FILE)

    def save_cookies(self, location: str):
        pickle.dump(self.get_cookies(), open(location, "wb"))

    def load_cookies(self, location: str):
        cookies = pickle.load(open(location, "rb"))
        for cookie in cookies:
            self.add_cookie(cookie)

    def call(self):
        self.find_element(by=By.CLASS_NAME, value=f'btn-call').click()

    def put(self):
        self.find_element(by=By.CLASS_NAME, value=f'btn-put').click()