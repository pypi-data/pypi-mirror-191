class Signal:
    def __init__(self, signal):
        self.signal = signal
        self.cost = 0
        self.is_high_cost = True if self.cost >20000 else False