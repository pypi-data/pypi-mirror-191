from cpanlp.contract.contract import *

class Lease(Contract):
    accounts = []
    def __init__(self, parties=None, consideration=None,obligations=None, property_address=None):
        super().__init__(parties, consideration,obligations)
        self.property_address = property_address
        self.rent = consideration
        self.economic_benefits = True
        self.use_direction = True
        Lease.accounts.append(self)
    def definition(self):
        return "Paragraph 9 of IFRS 16 states that ‘a contract is, or contains, a lease if the contract conveys the right to control the use of an identified asset for a period of time in exchange for consideration"