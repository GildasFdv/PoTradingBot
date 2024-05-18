from .EventHandler import EventHandler
from Configuration import Configuration

class UpdateHistoryNewEventHandler(EventHandler):
    def process(self, data, candles):
        if not self.isValidUpdateHistoryNew(data):
            return
        candles[:] = list(reversed(data['candles']))  # timestamp open close high low
        candles.append([candles[-1][0] + Configuration.PERIOD, candles[-1][1], candles[-1][2], candles[-1][3], candles[-1][4]])
        for tstamp, value in data['history']:
            tstamp = int(float(tstamp))
            candles[-1][2] = value  # set close all the time
            if value > candles[-1][3]:  # set high
                candles[-1][3] = value
            elif value < candles[-1][4]:  # set low
                candles[-1][4] = value
            if tstamp % Configuration.PERIOD == 0:
                if tstamp not in [c[0] for c in candles]:
                    candles.append([tstamp, value, value, value, value])

    def isValidUpdateHistoryNew(self, data):
        return 'asset' in data and data['asset'] == Configuration.SYMBOL and 'period' in data and data['period'] == Configuration.PERIOD and 'candles' in data and 'history' in data