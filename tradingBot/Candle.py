class Candle:
    def __init__(self, po_table):
        self.time = po_table[0]
        self.open = po_table[1]
        self.close = po_table[2]
        self.high = po_table[3]
        self.low = po_table[4]

    def __str__(self):
        return f"Time: {self.time}, Open: {self.open}, Close: {self.close}, High: {self.high}, Low: {self.low}"