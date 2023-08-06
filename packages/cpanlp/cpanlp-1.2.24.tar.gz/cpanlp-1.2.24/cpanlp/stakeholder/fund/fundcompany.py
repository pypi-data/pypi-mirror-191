from cpanlp.stakeholder.stakeholder import *

class FundCompany(Stakeholder):
    def __init__(self, name=None, investment_strategy=None, type=None,capital=None, interests=None,power=None):
        super().__init__(name,type,capital, interests,power)
        self.investment_strategy = investment_strategy

    def describe(self):
        print("Name: {}".format(self.name))
        print("Type: {}".format(self.type))
