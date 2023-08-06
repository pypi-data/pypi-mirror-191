from cpanlp.environment.environment import *

class EconomicEnvironment(Environment):
    def __init__(self, economic_growth=None, inflation=None, unemployment=None, exchange_rate=None,interest_rate=None):
        super().__init__()
        self.economic_growth = economic_growth
        self.inflation = inflation
        self.unemployment = unemployment
        self.exchange_rate = exchange_rate
        self.interest_rate=interest_rate
    def set_gdp(self, gdp):
        self.factors["GDP"] = gdp
    
    def set_unemployment_rate(self, unemployment_rate):
        self.factors["unemployment_rate"] = unemployment_rate
        