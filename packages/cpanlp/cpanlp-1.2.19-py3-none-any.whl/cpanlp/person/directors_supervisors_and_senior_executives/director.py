from cpanlp.person.investor.shareholder import *
class Director(Shareholder):
    def __init__(self, name,shares=None,expected_return=None, risk_preference=None, portfolio=None,age=None, wealth=None,utility_function=None):
        super().__init__(name, shares,expected_return, risk_preference, portfolio,age, wealth,utility_function)
    def making_strategic_decisions(self):
        pass
    def overseeing_the_overall_management (self):
        pass
    