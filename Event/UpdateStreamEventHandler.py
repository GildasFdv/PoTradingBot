from .EventHandler import EventHandler
from Configuration import Configuration

class UpdateStreamEventHandler(EventHandler):
    def process(self, data, candles):
        if not self.isValidUpdateStream(data, candles):
            return
        currency, tstamp, value  = data[0]
        candles[-1][2] = value  # set close all the time
        if value > candles[-1][3]:  # set high
            candles[-1][3] = value
        elif value < candles[-1][4]:  # set low
            candles[-1][4] = value
        tstamp = int(float(data[0][1]))
        if tstamp >= candles[-1][0] + Configuration.PERIOD:
            candles.append([candles[-1][0] + Configuration.PERIOD, value, value, value, value])

    def isValidUpdateStream(self, data, candles):
        return isinstance(data, list) and isinstance(data[0], list) and len(data[0]) == 3 and data[0][0] == Configuration.SYMBOL and len(candles) > 0