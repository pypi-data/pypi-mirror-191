from cpanlp.environment.market_environment import *
class IndustryEnvironment(MarketEnvironment):
    def __init__(self,technology_trend=None,market_size=None,market_growth=None,consumer_demand=None, competition=None, supplier=None, intermediaries=None, regulations=None):
        super().__init__(market_size,market_growth,consumer_demand, competition, supplier, intermediaries, regulations)
        self.technology_trend = technology_trend

