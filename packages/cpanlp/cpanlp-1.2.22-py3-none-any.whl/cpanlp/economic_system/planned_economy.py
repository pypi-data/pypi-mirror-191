from cpanlp.economic_system.economic_system import *

class PlannedEconomy(EconomicSystem):
    def __init__(self, name: str, government: object):
        """
        Initializes a PlannedEconomy object with the given name and government.

        :param name: A string representing the name of the planned economy.
        :param government: An object representing the government in the planned economy.
        """
        super().__init__(name)
        self.government = government

    def get_demand(self, goods: str):
        """
        Returns the total demand for the specified goods as planned by the government.

        :param goods: A string representing the name of the goods.
        :return: The total demand for the specified goods as planned by the government.
        """
        return self.government.get_demand_plan(goods)

    def get_supply(self, goods: str):
        """
        Returns the total supply of the specified goods as planned by the government.

        :param goods: A string representing the name of the goods.
        :return: The total supply of the specified goods as planned by the government.
        """
        return self.government.get_supply_plan(goods)

    def set_price(self, goods: str, price: float):
        """
        Sets the price for the specified goods as planned by the government.

        :param goods: A string representing the name of the goods.
        :param price: A float representing the price of the goods as planned by the government.
        """
        self.government.set_price_plan(goods, price)
