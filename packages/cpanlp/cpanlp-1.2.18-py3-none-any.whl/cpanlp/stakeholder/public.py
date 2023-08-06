from cpanlp.stakeholder.stakeholder import *

class Public(Stakeholder):
    def __init__(self, name,type=None,capital=None, interests=None,power=None):
        super().__init__(name,type,capital, interests,power)
        self.voice=""