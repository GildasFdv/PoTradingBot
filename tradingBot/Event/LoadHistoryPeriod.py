from .EventHandler import EventHandler
from Configuration import Configuration
from .PoCandle import CandleIndex

class LoadHistoryPeriodEventHandler(EventHandler):
    def process(self, data, candles):
        if not self.isValidUpdateHistoryNew(data):
            return
        new_candles = list(reversed(data['data']))
        existing_times = {candle[CandleIndex.TIME] for candle in candles}
        
        for new_candle in new_candles:
            if new_candle['time'] not in existing_times:
                candles.append([
                    new_candle['time'], 
                    new_candle['open'], 
                    new_candle['close'], 
                    new_candle['high'], 
                    new_candle['low']
                ])

        candles.sort(key= lambda c: c[CandleIndex.TIME])
        
        errors = []

        for i in range(len(candles) - 1):
            error = candles[i][CandleIndex.TIME] + Configuration.PERIOD - candles[i+1][CandleIndex.TIME]
            if error != 0:
                errors.append(error)
        
        if len(errors) > 0:
            print(f'LoadHistoryPeriodEventHandler: integrity issue {errors}')
                    
        print(f"LoadHistoryPeriodEventHandler: processed, {len(candles)} candles in memory")

    def isValidUpdateHistoryNew(self, data):
        return 'asset' in data and data['asset'] == Configuration.SYMBOL and 'period' in data and data['period'] == Configuration.PERIOD and 'data' in data