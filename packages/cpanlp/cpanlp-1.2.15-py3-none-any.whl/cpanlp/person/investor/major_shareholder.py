from cpanlp.person.investor.shareholder import *

class MajorShareholder(Shareholder):
    def __init__(self, name, age=None, wealth=None,utility_function=None,portfolio=None, expected_return=None, risk_preference=None,shares=None, voting_power=None):
        super().__init__(name, age, wealth,utility_function,portfolio, expected_return, risk_preference,shares)
        self.voting_power = voting_power