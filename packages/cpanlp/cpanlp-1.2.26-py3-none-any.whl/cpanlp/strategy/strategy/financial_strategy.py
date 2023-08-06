from cpanlp.strategy.strategy.strategy import *

#财务杠杆是指公司使用借贷来提高资产收益率的策略。
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
if __name__ == '__main__':
    main()
