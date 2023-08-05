from cpanlp.person.supervisor import *

class Auditor(Supervisor):
    def __init__(self, name, age=None,wealth=None,utility_function=None):
        super().__init__(name, age,wealth,utility_function)