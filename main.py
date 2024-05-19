from PoDataManager import PoDataManager
from PoDriver import PoDriver
from MLIndicator import MLIndicator
from threading import Lock

def menu():
    print("Press 'a' to activate MLIndicator")
    print("Press 'd' to deactivate MLIndicator")
    print("Press 's' to show state")
    print("Press 'q' to quit")

if __name__ == "__main__":
    
    candles = []
    candles_lock = Lock()
    poDriver = PoDriver()
    dataManager = PoDataManager([poDriver, candles_lock ,candles])
    dataManager.start()
    mlIndicator = MLIndicator([poDriver, candles_lock ,candles])
    mlIndicator.start()
    try:
        menu()
        while True:
            key = input()
            if key == 'q':
                break
            elif key == 'a':
                mlIndicator.activated = True
            elif key == 'd':
                mlIndicator.activated = False
            elif key == 's':
                print(f'State: {'active' if mlIndicator.activated == True else 'inactive'}')
    except KeyboardInterrupt:
        pass
    finally:
        dataManager.stop()
        mlIndicator.stop()
        dataManager.join()
        mlIndicator.join()