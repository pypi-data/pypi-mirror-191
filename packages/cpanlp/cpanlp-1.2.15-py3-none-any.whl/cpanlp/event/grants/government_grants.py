class GovernmentGrants:
    def __init__(self, year, grant_name, grant_amount):
        self.year = year
        self.grant_name = grant_name
        self.grant_amount = grant_amount
        
    def __str__(self):
        return "Government Grants: Year - {}, Grant Name - {}, Grant Amount - {}".format(
            self.year, self.grant_name, self.grant_amount
        )
        
    def increase_amount(self, amount):
        self.grant_amount += amount