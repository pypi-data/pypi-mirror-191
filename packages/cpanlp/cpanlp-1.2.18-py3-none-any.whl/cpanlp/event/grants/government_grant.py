from cpanlp.event.grants.grant import *

class GovernmentGrant(Grant):
    def __init__(self, recipient=None, donor=None, amount=None, purpose=None, deadline=None,year=None):
        super().__init__(recipient, donor, amount, purpose, deadline)
        self.year = year
    def __str__(self):
        return "Government Grants: Year - {}, Grant Name - {}, Grant Amount - {}".format(
            self.year, self.grant_name, self.grant_amount
        )
        
    def increase_amount(self, amount):
        self.grant_amount += amount