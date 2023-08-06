from cpanlp.contract.financial_instrument.financial_instrument import *
from cpanlp.account.liabilities.liability import *
class FinancialLiability(Liability,FinancialInstrument):
    accounts = []
    def __init__(self, account, credit, date,due_date,rate,parties, consideration, obligations,value):
        Liability.__init__(self, account, credit, date,due_date,rate)
        FinancialInstrument.__init__(self,parties, consideration,obligations, value)
        FinancialLiability.accounts.append(self)

