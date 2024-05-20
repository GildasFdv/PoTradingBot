from threading import Thread
from enum import IntEnum
from time import sleep
from Event.PoCandle import Candle, CandleIndex
import pandas as pd
from indicators import *
from joblib import load

class MLIndicatorParams(IntEnum):
    PO_DRIVER = 0
    CANDLES_LOCK = 1
    CANDLES = 2

class MLIndicator(Thread):

    def __init__(self, args):
        self.running = True
        self.activated = False
        self.last_timestamp = 0
        self.threshlod = 0.67
        Thread.__init__(self, args=args, name='MLIndicator')
        self.poDriver = args[MLIndicatorParams.PO_DRIVER]
        self.candles_lock = args[MLIndicatorParams.CANDLES_LOCK]
        self.candles_lock.acquire()
        self.candles = args[MLIndicatorParams.CANDLES]
        self.candles_lock.release()
        print("MLIndicator: loading model...")
        self.model = load('model_eurusd_otc.joblib') 
        print("MLIndicator: model loaded")

    def run(self):
        print("MLIndicator: started")
        while self.running:
            currentSymbol = self.poDriver.getCurrentSymbol()
            if not self.activated or self.threshlod < 0.5 or currentSymbol != Configuration.SYMBOL:
                print(f'Incorrect current symbol: {currentSymbol}')
                continue
            try:
                self.candles_lock.acquire()
                if len(self.candles) > 79 and self.candles[-2][CandleIndex.TIME] > self.last_timestamp:
                    self.last_timestamp = self.candles[-2][CandleIndex.TIME]

                    data = pd.DataFrame(data=self.candles[-79:-1], columns=['time', 'open', 'close', 'high', 'low'])
                    data.set_index('time', inplace=True)

                    # bollinger bands
                    data['bb_basis'], data['bb_upper'], data['bb_lower'] = bollinger_bands(data[['close']], 20)

                    # macd
                    data['macd_ema'] = macd(data[['close']], 12, 26)
                    data['macd_sma'] = macd(data[['close']], 12, 26, True)
                    data['macd_signal_ema'] = macd_signal(data[['macd_ema']], 9)
                    data['macd_signal_sma'] = macd_signal(data[['macd_sma']], 9, True)

                    # rsi
                    data['rsi_9'] = rsi(data[['close']], 9)
                    data['rsi_14'] = rsi(data[['close']], 14)
                    data['rsi_28'] = rsi(data[['close']], 28)

                    # stochastique
                    data['stochastique'] = stochastique(data[['close']], 14)
                    data['stochastique_signal'] = stochastique_signal(data[['stochastique']], 14)

                    # ichimoku
                    data['tekan_sen'] = sen(data[['close']] ,9)
                    data['kujin_sen'] = sen(data[['close']] ,26)
                    data['senko_A'] = senko_span_A(data['tekan_sen'], data['kujin_sen'], 26)
                    data['senko_B'] = senko_span_B(data[['close']], 52, 26)

                    print(data.tail(n=1))

                    probas = self.model.predict_proba(data.tail(n=1))

                    call, even, put = probas[0]

                    if call > self.threshlod:
                        self.poDriver.call()

                    if put > self.threshlod:
                        self.poDriver.put()

                    print(f"MLIndicator: call={call}, even={even}, put={put}")


            except Exception as e:
                print("MLIndicator: an error occured while processing the data")
                print(e)
            finally:    
                self.candles_lock.release()

                

    def stop(self):
        self.running = False
        print("MLIndicator: stopped")

    def process(self, candle: Candle):
        pass