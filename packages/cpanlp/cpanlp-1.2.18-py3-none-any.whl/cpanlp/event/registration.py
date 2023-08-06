class Registration:
    def __init__(self, decision=None, time=None):
        self.decision = decision
        self.time = time
    def is_uncertain(self):
        return self.decision is None or self.time is None
