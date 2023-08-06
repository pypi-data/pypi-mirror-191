from cpanlp.event.acquisition.merger import *

class StrategicMerger(Merger):
    def __init__(self, target_company, acquiring_company, merger_price=None,strategic_goals=None,date=None):
        super().__init__(target_company, acquiring_company, merger_price,date)
        self.strategic_goals = strategic_goals