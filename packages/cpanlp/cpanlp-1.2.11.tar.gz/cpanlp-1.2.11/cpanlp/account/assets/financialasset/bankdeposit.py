from cpanlp.account.assets.financialasset.financialasset import *
from datetime import datetime

class Bankdeposit(FinancialAsset):
    accounts = []
    def __init__(self, account, debit,date,parties, consideration, obligations,value, interest_rate):
        super().__init__(account, debit,date,parties, consideration, obligations,value)
        self.interest_rate = interest_rate
        Bankdeposit.accounts.append(self)
    def get_interest_earned(self, end_date: str) -> float:
        end_date1 = datetime.strptime(end_date, "%Y-%m-%d").date()
        start_date1 = datetime.strptime(self.date, "%Y-%m-%d").date()
        return (end_date1 - start_date1).days * self.interest_rate * self.debit
# 金融资产的交易性金融资产是指具有流动性和可转移性的金融资产，如股票、债券、期货和外汇等。
