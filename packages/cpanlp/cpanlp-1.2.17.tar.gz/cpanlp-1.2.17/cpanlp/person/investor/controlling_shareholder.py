from cpanlp.person.investor.shareholder import *

class ControllingShareholder(Shareholder):
    def __init__(self, name, control_percentage=None,age=None, wealth=None,utility_function=None,portfolio=None, expected_return=None, risk_preference=None,shares=None):
        super().__init__(name, age, wealth,utility_function,portfolio, expected_return, risk_preference,shares)
        self.control_percentage = control_percentage