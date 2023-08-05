from cpanlp.account.assets.financialasset.financialasset import *

class Bond(FinancialAsset):
    accounts = []
    def __init__(self, account, debit,parties,value, rate, currency=None,domestic=None,date=None,consideration=None, obligations=None,outstanding_balance=None):
        super().__init__(account, debit,date,parties, consideration, obligations,value)
        self.rate = rate
        self.currency = currency
        self.domestic = domestic
        self.outstanding_balance = outstanding_balance
        Bond.accounts.append(self)