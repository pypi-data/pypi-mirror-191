#初始化，创建一个 Hedging 类的实例时需要传递基础资产、期货合约、期货价格和基础资产价格。
#calculate_hedging_ratio，计算套期保值比率，即基础资产价格除以期货价格。
#calculate_hedging_quantity，计算套期保值数量，即根据套期保值比率和投资的仓位大小计算出需要买入的期货数量。
#calculate_hedging_cost，计算套期保值成本，即需要花费的期货价格。

class Hedging:
    def __init__(self, underlying_asset, futures_contract, futures_price, underlying_price):
        self.underlying_asset = underlying_asset
        self.futures_contract = futures_contract
        self.futures_price = futures_price
        self.underlying_price = underlying_price

    def calculate_hedging_ratio(self):
        return self.underlying_price / self.futures_price

    def calculate_hedging_quantity(self, position_size):
        return position_size / self.calculate_hedging_ratio()

    def calculate_hedging_cost(self, position_size):
        return self.calculate_hedging_quantity(position_size) * self.futures_price
