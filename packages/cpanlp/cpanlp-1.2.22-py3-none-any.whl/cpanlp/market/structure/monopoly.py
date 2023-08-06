from cpanlp.market.market import *

class Monopoly(Market):
    def __init__(self, commodity, businessentity):
        super().__init__(commodity, [])
        self.businessentity=businessentity
        self.profit_maximizing_price = None
        self.profit_maximizing_quantity = None
        self.market_demand = None
        self.total_cost = None
        self.barriers = True
        self.free_entry = False