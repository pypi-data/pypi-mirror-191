from cpanlp.account.assets.financialasset.financialasset import *
from datetime import datetime
class AccountsReceivable(FinancialAsset):
    accounts = []
    def __init__(self,account, debit,date,parties, consideration, obligations,value, due_date):
        super().__init__(account, debit,date,parties, consideration, obligations,value)
        self.due_date = due_date
        self.due_dates = {}
        AccountsReceivable.accounts.append(self)
    def add_receivable(self, value, due_date):
        self.debit += value
        self.due_dates[due_date] = value
    def reduce_receivable(self, value, due_date):
        self.debit -= value
        self.due_dates[due_date] -= value
    def check_due_date(self, date):
        total_due = 0
        date = datetime.strptime(date, "%Y-%m-%d").date()
        for d, v in self.due_dates.items():
            d = datetime.strptime(d, "%Y-%m-%d").date()
            if d <= date:
                total_due += v
        return total_due
class DividendReceivable(AccountsReceivable):
    accounts = []
    def __init__(self, account, debit,date,parties, consideration, obligations,value, due_date):
         super().__init__(account, debit,date,parties, consideration, obligations,value, due_date)
         DividendReceivable.accounts.append(self)
def main():
    print(5)
if __name__ == '__main__':
    main()