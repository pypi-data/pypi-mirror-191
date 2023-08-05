from cpanlp.person.consumer import *

class Fiduciary(Consumer):
    def __init__(self, name, beneficiary=None, age=None,wealth=None, utility_function=None):
        super().__init__(name, age,wealth, utility_function)
        self.beneficiary = beneficiary