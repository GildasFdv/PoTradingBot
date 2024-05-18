from threading import Thread
from enum import IntEnum
from time import sleep
from Candle import Candle

class MLIndicatorParams(IntEnum):
    CANDLES_LOCK = 0
    CANDLES = 1

class MLIndicator(Thread):

    def __init__(self, args):
        self.running = True
        Thread.__init__(self, args=args, name='MLIndicator')
        self.candles_lock = args[MLIndicatorParams.CANDLES_LOCK]
        self.candles_lock.acquire()
        self.candles = args[MLIndicatorParams.CANDLES]
        self.candles_lock.release()

        self.last_timestamp = 0

    def run(self):
        print("MLIndicator: started")
        while self.running:
            sleep(1)
            self.candles_lock.acquire()
            if len(self.candles) > 1 and self.candles[-2][0] > self.last_timestamp:
                candle = Candle(self.candles[-2])
                self.last_timestamp = candle.time
                print(candle)
            self.candles_lock.release()
            

    def stop(self):
        self.running = False
        print("MLIndicator: stopped")