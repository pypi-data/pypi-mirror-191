from cpanlp.event.acquisition.acquisition import *

class HostileAcquisition(Acquisition):
    def __init__(self, target_company, acquiring_company,acquisition_ratio=None,hostile_tactic=None,price=None,leverage_ratio=None,date=None):
        super().__init__(target_company, acquiring_company, acquisition_ratio, price,leverage_ratio,date)
        self.hostile_tactic = hostile_tactic