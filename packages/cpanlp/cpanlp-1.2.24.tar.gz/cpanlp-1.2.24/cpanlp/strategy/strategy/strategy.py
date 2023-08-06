from cpanlp.decorator.witheffects import *
class Strategy:
    def __init__(self, company, market_focus, impact,time_horizon):
        self.company = company
        self.time_horizon = time_horizon
        self.market_focus = market_focus
        self.impact = impact
        self.decision = None
