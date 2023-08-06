from cpanlp.economic_system.economic_system import *

class MarketEconomy(EconomicSystem):
    def __init__(self, name: str, citizens: list, businesses: list):
        """
        Initializes a MarketEconomy object with the given name and citizens and businesses.

        :param name: A string representing the name of the market economy.
        :param citizens: A list of citizens who participate in the economy.
        :param businesses: A list of businesses that participate in the economy.
        """
        super().__init__(name)
        self.citizens = citizens
        self.businesses = businesses

    def get_demand(self, goods: str):
        """
        Returns the total demand for the specified goods by the citizens and businesses.

        :param goods: A string representing the name of the goods.
        :return: The total demand for the specified goods.
        """
        total_demand = 0
        for citizen in self.citizens:
            total_demand += citizen.get_demand(goods)
        for business in self.businesses:
            total_demand += business.get_demand(goods)
        return total_demand

    def get_supply(self, goods: str):
        """
        Returns the total supply of the specified goods by the businesses.

        :param goods: A string representing the name of the goods.
        :return: The total supply of the specified goods.
        """
        total_supply = 0
        for business in self.businesses:
            total_supply += business.get_supply(goods)
        return total_supply

    def set_price(self, goods: str, price: float):
        """
        Sets the price for the specified goods.

        :param goods: A string representing the name of the goods.
        :param price: A float representing the price of the goods.
        """
        for business in self.businesses:
            business.set_price(goods, price)
