from cpanlp.environment.market_environment import *
class IndustryEnvironment(MarketEnvironment):
    def __init__(self,technology_trend=None,market_size=None,market_growth=None,consumer_demand=None, competition=None, supplier=None, intermediaries=None, regulations=None):
        super().__init__(market_size,market_growth,consumer_demand, competition, supplier, intermediaries, regulations)
        self.technology_trend = technology_trend

def main():
    industry_env = IndustryEnvironment(competition="Intense", technology_trend="Rapid", regulations="Strict")
    print(industry_env.competition)
if __name__ == '__main__':
    main()