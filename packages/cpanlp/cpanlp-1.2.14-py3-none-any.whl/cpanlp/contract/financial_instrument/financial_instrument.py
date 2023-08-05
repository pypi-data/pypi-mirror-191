from cpanlp.contract.contract import *
class FinancialInstrument(Contract):
    accounts = []
    def __init__(self,parties=None, consideration=None,obligations=None, value=None):
        super().__init__(parties, consideration,obligations)
        self.value = value
        FinancialInstrument.accounts.append(self)
