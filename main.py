from PoDataManager import PoDataManager
from PoDriver import PoDriver
from MLIndicator import MLIndicator
from threading import Lock

if __name__ == "__main__":
    
    candles = []
    candles_lock = Lock()
    poDriver = PoDriver()
    dataManager = PoDataManager([poDriver, candles_lock ,candles])
    mlIndicator = MLIndicator([candles_lock ,candles])
    dataManager.start()
    mlIndicator.start()
    try:
        input("Press Enter to stop the bot\n")
    except KeyboardInterrupt:
        pass
    finally:
        dataManager.stop()
        mlIndicator.stop()
        dataManager.join()
        mlIndicator.join()