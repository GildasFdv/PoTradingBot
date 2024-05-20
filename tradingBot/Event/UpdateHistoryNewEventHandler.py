from .EventHandler import EventHandler
from Configuration import Configuration
from .PoCandle import CandleIndex

class UpdateHistoryNewEventHandler(EventHandler):
    def process(self, data, candles):
        if not self.isValidUpdateHistoryNew(data):
            return
        candles[:] = list(reversed(data['candles']))  # timestamp open close high low
        candles.append([candles[-1][CandleIndex.TIME] + Configuration.PERIOD, 
                        candles[-1][CandleIndex.OPEN],
                        candles[-1][CandleIndex.CLOSE], 
                        candles[-1][CandleIndex.HIGH], 
                        candles[-1][CandleIndex.LOW]])
        for tstamp, value in data['history']:
            tstamp = int(float(tstamp))
            candles[-1][CandleIndex.CLOSE] = value  # set close all the time
            if value > candles[-1][CandleIndex.HIGH]:  # set high
                candles[-1][CandleIndex.HIGH] = value
            elif value < candles[-1][CandleIndex.LOW]:  # set low
                candles[-1][CandleIndex.LOW] = value
            if tstamp % Configuration.PERIOD == 0:
                if tstamp not in [c[CandleIndex.TIME] for c in candles]:
                    candles.append([tstamp, value, value, value, value])
        print(f"UpdateHistoryNewEventHandler: processed, {len(candles)} candles in memory")

    def isValidUpdateHistoryNew(self, data):
        return 'asset' in data and data['asset'] == Configuration.SYMBOL and 'period' in data and data['period'] == Configuration.PERIOD and 'candles' in data and 'history' in data