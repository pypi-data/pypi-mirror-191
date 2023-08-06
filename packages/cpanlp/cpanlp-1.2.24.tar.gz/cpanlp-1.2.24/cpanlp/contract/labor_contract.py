from cpanlp.contract.contract import *
class LaborContract(Contract):
    accounts = []
    def __init__(self,employee=None,employer=None, parties=None, consideration=None,obligations=None,salary=None):
        super().__init__(parties, consideration,obligations)
        self.employee = employee
        self.employer = employer
        self.salary = salary
        LaborContract.accounts.append(self)