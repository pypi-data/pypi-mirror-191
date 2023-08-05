from cpanlp.person.consumer import *

class Craftsman(Consumer):
    def __init__(self, name,skill_level=None, age=None,wealth=None,utility_function=None):
        super().__init__(name, age,wealth,utility_function)
        self.skill_level = skill_level
        self.projects = []