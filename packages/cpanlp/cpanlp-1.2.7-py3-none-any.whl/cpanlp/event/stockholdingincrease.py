#Whether to represent an increase in a company's stock holdings as a class or a method of a class depends on the specific requirements of your project and how you want to design your program.

#If the increase in stock holdings is a standalone event that can be treated independently, then it might be appropriate to represent it as a separate class. For example, if you need to track multiple increases in stock holdings made by different directors and senior managers, you can create separate instances of the StockHoldingIncrease class for each event.
class StockHoldingIncrease:
    def __init__(self, name, position, shares_held, shares_added):
        self.name = name
        self.position = position
        self.shares_held = shares_held
        self.shares_added = shares_added