from cpanlp.account.assets.financialasset.financialasset import *

class Stock(FinancialAsset):
    accounts = []
    def __init__(self, account, debit,date,parties, consideration, obligations,value,market_value,symbol):
        super().__init__(account, debit,date,parties, consideration, obligations,value)
        self.market_value=market_value
        self.symbol = symbol
        Stock.accounts.append(self)
    def sell(self, amount):
        if amount > self.debit:
            raise ValueError("Cannot sell more than the current value of the asset.")
        self.debit -= amount
    def buy(self, amount):
        self.debit += amount
    def __str__(self):
        return f"Stock(account='{self.account}', value={self.debit}, symbol='{self.symbol}', market='{self.market_value}')"