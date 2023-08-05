from cpanlp.stakeholder.stakeholder import *

class Media(Stakeholder):
    def __init__(self, name,type=None,capital=None, interests=None,power=None):
        super().__init__(name,type,capital, interests,power)
        self.publish=""