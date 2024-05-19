from .EventHandler import EventHandler
from Configuration import Configuration
from .PoCandle import CandleIndex

class UpdateStreamEventHandler(EventHandler):
    def process(self, data, candles):
        if not self.isValidUpdateStream(data, candles):
            return
        currency, tstamp, value  = data[0]
        candles[-1][CandleIndex.CLOSE] = value  # set close all the time
        if value > candles[-1][CandleIndex.HIGH]:  # set high
            candles[-1][CandleIndex.HIGH] = value
        elif value < candles[-1][CandleIndex.LOW]:  # set low
            candles[-1][CandleIndex.LOW] = value
        tstamp = int(float(data[0][1]))
        if tstamp >= candles[-1][CandleIndex.TIME] + Configuration.PERIOD:
            candles.append([candles[-1][CandleIndex.TIME] + Configuration.PERIOD, value, value, value, value])

    def isValidUpdateStream(self, data, candles):
        return isinstance(data, list) and isinstance(data[0], list) and len(data[0]) == 3 and data[0][0] == Configuration.SYMBOL and len(candles) > 0