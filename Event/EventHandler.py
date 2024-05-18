class EventHandler:
    def process(self, data, candles):
        raise NotImplementedError("Subclasses should implement this!")
    
class EventManager:
    def __init__(self):
        self.events = {}
        self.current_event = None

    def registerEventHandler(self, event_name, event_handler):
        self.events[event_name] = event_handler

    def handleEvent(self, data, candles):
        if self.current_event is not None:
            self.events[self.current_event].process(data, candles)
            self.current_event = None

    def setEventReceived(self, event_name):
        if event_name in self.events:
            self.current_event = event_name

    def isEventReceived(self):
        return self.current_event is not None