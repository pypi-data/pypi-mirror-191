from cpanlp.department.department import *
class SupervisoryBoard(Department):
    def __init__(self,name, goals=None, incentives=None):
        super().__init__(name, goals, incentives)
        self.members = []