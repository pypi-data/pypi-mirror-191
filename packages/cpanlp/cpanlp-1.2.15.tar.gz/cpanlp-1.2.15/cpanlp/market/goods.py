from cpanlp.market.commodity import *
class Goods(Commodity):
    def __init__(self, goods, fair_value,market_price, supply, demand):
        super().__init__(None, fair_value,market_price, supply, demand)
        self.goods=goods