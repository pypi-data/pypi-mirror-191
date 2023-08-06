from typing import List
from cpanlp.contract.financial_instrument.financial_instrument import *
import pandas as pd
#The most important attribute of equity is its ability to represent the residual ownership interest in a company after all liabilities have been paid. This means that equity represents the value of a company that is left over for shareholders after all debts have been settled. Other important attributes of equity include its growth potential, as well as its risk and return characteristics. Additionally, factors such as the level of diversification, liquidity, and the quality of the underlying assets also important to consider when evaluating equity.
class Equity(FinancialInstrument):
    accounts = []
    def __init__(self, account, credit,date,parties, consideration, obligations,value):
        super().__init__(parties, consideration, obligations,value)
        self.credit=credit
        self.account = account
        self.date = date
        self.residual_ownership_interest=None
        self.growth_pontential=None
        self.risk_return = None
        self.diversification = None
        self.liquidity = None
        self.quality_of_underlying_assets=None
        Equity.accounts.append(self)
    def __str__(self):
        return f"{self.account}: {self.value}"
    @classmethod
    def withdraw(cls, account, value):
        for equity in Equity.accounts:
            if equity.account == account:
                equity.value -= value
                break
    @classmethod
    def sum(cls):
        data = [[asset.account, asset.date, asset.credit] for asset in Equity.accounts]
        df = pd.DataFrame(data, columns=['账户类别', '日期', '贷方金额'])
        return df

def main():
    a=Equity("jack",22000,"2025-01-01",None,None,"信托责任",22000)
    b=Equity("jack1",22000,"2025-01-01",None,None,"信托责任",20000)
    Equity.withdraw("jack",10000)
    print(a.value)
    print(Equity.sum())
    print(len(Equity.accounts))
if __name__ == '__main__':
    main()