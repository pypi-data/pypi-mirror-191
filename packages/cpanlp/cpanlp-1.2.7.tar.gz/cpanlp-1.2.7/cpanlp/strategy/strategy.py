from cpanlp.decorator.witheffects import *
class Strategy:
    def __init__(self, company, market_focus, impact,time_horizon):
        self.company = company
        self.time_horizon = time_horizon
        self.market_focus = market_focus
        self.impact = impact
        self.decision = None
#财务杠杆是指公司使用借贷来提高资产收益率的策略。
class Long_term_strategy(Strategy):
    def __init__(self, company, market_focus, impact,time_horizon):
        super().__init__(company, market_focus, impact,time_horizon)
        self.long_term_impact = sum(impact.values()) if time_horizon > 1 else None
class FinancialStrategy(Strategy):
    def __init__(self, company, market_focus, impact,time_horizon):
        super().__init__(company, market_focus, impact,time_horizon)
    @with_side_effects(["Increased risk of default.","Amplified losses","Increased volatility","Difficulty in repaying debt","Reduced flexibility"])
    def leverage_strategy(self,total_debt, total_equity):
        leverage_ratio = total_debt / total_equity
        return leverage_ratio
    #毒丸计划(Poison Pill)是指公司采取的一种防御策略，用于阻止其他公司对其进行恶意收购。毒丸计划通常是通过增加公司的股票数量来降低股票价格，使收购变得更加困难。
    @with_side_effects(["Harm the company's reputation and relationships with investors."])
    def poison_pill(self,shares_outstanding, dilution_factor):
        new_shares_outstanding = shares_outstanding * (1 + dilution_factor)
        return new_shares_outstanding
def main():
    a=FinancialStrategy("huawei","growth",15,19)
    print(a.leverage_strategy(100,20))
    b=Long_term_strategy("Tesla","defense",{"Increased risk of default":199,"Increased volatility":-19},5)
    print(b.long_term_impact)
if __name__ == '__main__':
    main()
