from cpanlp.event.acquisition.acquisition import *

class StrategicMerger(Acquisition):
    def __init__(self, target_company, acquiring_company,acquisition_ratio=None,strategic_goals=None,price=None,leverage_ratio=None,date=None):
        super().__init__(target_company, acquiring_company, acquisition_ratio, price,leverage_ratio,date)
        self.strategic_goals = strategic_goals