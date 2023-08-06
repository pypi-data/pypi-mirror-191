#the most important attribute of a commodity is its ability to be accurately valued and measured. This is important because commodities are often bought and sold on a regular basis, and their value can fluctuate significantly based on market conditions. Other important attributes include the commodity's level of standardization, as well as its ease of storage and transport. Additionally, factors such as the commodity's level of substitutability and the level of competition in the market are also important to consider when evaluating a commodity in accounting.
class Commodity:
    def __init__(self, commodity, fair_value,market_price, supply, demand):
        self.commodity = commodity
        self.fair_value = fair_value
        self.market_price =market_price
        self.supply = supply
        self.demand = demand
        self.gap = self.demand - self.supply
        self.supply_curve = {}
        self.demand_curve = {}
        self.level_of_standardization = None
        self.ease_of_storage = None
        self.ease_of_transport = None
        self.level_of_substitutability = None
        self.level_of_competition = None
        self.fluctuation = None
    def info(self):
        print(f"Commodity: {self.commodity}")
        print(f"Fair value: {self.fair_value}")
        print(f"Supply: {self.supply}")
        print(f"Demand: {self.demand}")
    def price_trend(self):
        if self.supply > self.demand:
            print(f"The price of {self.commodity} is expected to decrease in the future")
        elif self.supply < self.demand:
            print(f"The price of {self.commodity} is expected to increase in the future")
        else:
            print(f"The price of {self.commodity} is expected to remain stable in the future")
    def get_supply_curve(self):
        print(f"The supply curve for {self.commodity} is as follows:")
        for price, quantity in self.supply_curve.items():
            print(f"Price: {price}, Quantity: {quantity}")   
    def get_demand_curve(self,demand_curve):
        print(f"The demand curve for {self.commodity} is as follows:")
        for price, quantity in demand_curve.items():
            print(f"Price: {price}, Quantity: {quantity}")
#Goods generally refers to any items that are produced or manufactured and then sold to consumers, such as clothing, electronics, or food.Commodity, on the other hand, typically refers to raw materials or primary products that are sold in bulk, such as crops, minerals, or oil. Commodities are often traded on commodity markets, and their prices can be affected by factors such as weather conditions, supply and demand, and geopolitical events.


def main():
    print("hi")
if __name__ == '__main__':
    main()