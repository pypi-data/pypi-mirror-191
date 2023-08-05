from cpanlp.person.consumer import *

class Creditor(Consumer):
    def __init__(self, name, amount=None, age=None, wealth=None,utility_function=None):
        super().__init__(name, age, wealth,utility_function)
        self.amount = amount
