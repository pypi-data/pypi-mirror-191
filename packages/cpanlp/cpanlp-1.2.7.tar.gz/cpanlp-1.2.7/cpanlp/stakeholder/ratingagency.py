from cpanlp.stakeholder.stakeholder import *

class RatingAgency(Stakeholder):
    def __init__(self, name,type=None,capital=None,interests=None,power=None):
        super().__init__(name,type,capital, interests,power)
        self.ratings = {}
    def assign_rating(self, company, rating):
        self.ratings[company.name] = rating