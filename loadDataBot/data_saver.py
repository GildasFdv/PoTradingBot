from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pickle
from time import sleep
import json
import base64

service = Service()
options = Options()
options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
driver = webdriver.Chrome(service=service, options=options)

# URL de la page de connexion
url = 'https://pocketoption.com/fr/cabinet/demo-quick-high-low/'

# Fonction pour sauvegarder les cookies
def save_cookies(driver, location):
    pickle.dump(driver.get_cookies(), open(location, "wb"))

# Fonction pour charger les cookies
def load_cookies(driver, location):
    cookies = pickle.load(open(location, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

# Emplacement du fichier de cookies
cookies_file = 'path_to_cookies.pkl'

# Essayez de charger les cookies et accédez à la page
try:
    driver.get(url)
    load_cookies(driver, cookies_file)
    driver.get(url)  # Rechargez la page avec les cookies chargés
except FileNotFoundError:
    # Si les cookies ne sont pas trouvés, connectez-vous manuellement et sauvegardez les cookies
    driver.get(url)
    # Ajoutez ici le code pour vous connecter manuellement ou attendez que vous vous connectiez manuellement
    sleep(10)  # Attendre que l'utilisateur se connecte manuellement
    save_cookies(driver, cookies_file)

def websocket_log(number):
    for wsData in driver.get_log('performance'):
        message = json.loads(wsData['message'])['message']
        response = message.get('params', {}).get('response', {})
        if response.get('opcode', 0) == 2:
            payload_str = base64.b64decode(response['payloadData']).decode('utf-8')
            data = json.loads(payload_str)
            if payload_str.startswith('{"asset":"EURUSD"'): 
                candles = None
                if 'candles' in data:
                    candles = data['candles']
                elif 'data' in data: 
                    candles = data['data']
                with open(f'po_data/po_data_{number}.json', 'w') as file: 
                        file.write(json.dumps(candles))
                        number = number + 1

    return number
    


# Votre code de navigation continue ici
number = 0
while True:
    
    number = websocket_log(number)