from cpanlp.strategy.strategy.strategy import *
class LongTermStrategy(Strategy):
    def __init__(self, company, market_focus, impact,time_horizon):
        super().__init__(company, market_focus, impact,time_horizon)
        self.long_term_impact = sum(impact.values()) if time_horizon > 1 else None

def main():
    b=LongTermStrategy("Tesla","defense",{"Increased risk of default":199,"Increased volatility":-19},5)
    print(b.long_term_impact)
if __name__ == '__main__':
    main()
