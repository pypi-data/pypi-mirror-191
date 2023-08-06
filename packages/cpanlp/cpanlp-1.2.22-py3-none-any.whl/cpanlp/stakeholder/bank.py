from cpanlp.stakeholder.stakeholder import *

class Bank(Stakeholder):
    def __init__(self, name,type=None,capital=None, interests=None,power=None):
        super().__init__(name,type,capital, interests,power)
        self.loans = {}
    def grant_loan(self, company, amount):
        self.loans[company.name] = amount
        