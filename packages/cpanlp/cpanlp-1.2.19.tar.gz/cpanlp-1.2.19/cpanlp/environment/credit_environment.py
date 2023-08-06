from cpanlp.environment.economic_environment import *

class CreditEnvironment(EconomicEnvironment):
    def __init__(self,interest_rate=None,default_rate=None,economic_growth=None, inflation=None, unemployment=None, exchange_rate=None):
        super().__init__(economic_growth, inflation, unemployment, exchange_rate,interest_rate)
        self.add_factor("interest_rate", 0)
        self.add_factor("default_rate", 0)
        