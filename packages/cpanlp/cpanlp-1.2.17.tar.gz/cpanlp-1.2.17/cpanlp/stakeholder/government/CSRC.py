from cpanlp.stakeholder.government.government import *

class CSRC(Government):
    def __init__(self,name,type=None,capital=None, interests=None,power=None):
        super().__init__(name,type,capital, interests,power)
        self.registration_list = []

    def register(self, company):
        self.registration_list.append(company)

    def approve(self, company):
        for c in self.registration_list:
            if c == company:
                c.approve()
                break

    def reject(self, company):
        for c in self.registration_list:
            if c == company:
                c.reject()
                break
