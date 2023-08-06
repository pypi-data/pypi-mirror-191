from cpanlp.person.consumer import *

class Partner(Consumer):
    def __init__(self, name,share=None, age=None,wealth=None,utility_function=None):
        super().__init__(name, age,wealth,utility_function)
        self.share = share