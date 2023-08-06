from cpanlp.account.assets.asset import *
class InvestmentProperty(Asset):
    accounts = []
    def __init__(self, account, debit, date,tenant,address,income):
        super().__init__(account, debit, date)
        self.address = address
        self.income = income
        self.tenant = tenant
        InvestmentProperty.accounts.append(self)
    @classmethod
    def sum(cls):
        data = [[asset.account, asset.date, asset.debit] for asset in InvestmentProperty.accounts]
        df = pd.DataFrame(data, columns=['账户类别', '日期', '借方金额'])
        return df
    
        