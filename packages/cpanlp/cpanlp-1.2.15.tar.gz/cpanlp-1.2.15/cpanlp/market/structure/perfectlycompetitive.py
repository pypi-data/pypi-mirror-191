from cpanlp.market.market import *
import math

class PerfectlyCompetitive(Market):
    def __init__(self, commodity, participants):
        #price takers
        super().__init__(commodity, participants)
        self.equilibrium_price = None
        self.equilibrium_quantity = None
        self.barriers = False
        self.free_entry = True
        self.number_of_participants = math.inf
    def calculate_equilibrium(self):
        # Code to calculate equilibrium price and quantity
        pass