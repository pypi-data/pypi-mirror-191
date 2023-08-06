class PrivatePlacement:
    def __init__(self, company=None, stock_price=None, shares_offered=None, investors=None, confidentiality=None, cost=None, return_on_investment=None, customization=None):
        self.company = company
        self.stock_price = stock_price
        self.shares_offered = shares_offered
        self.investors = investors
        self.confidentiality = confidentiality
        self.cost = cost
        self.return_on_investment = return_on_investment
        self.customization = customization

    def set_company(self, company):
        self.company = company

    def set_stock_price(self, stock_price):
        self.stock_price = stock_price

    def set_shares_offered(self, shares_offered):
        self.shares_offered = shares_offered

    def set_investors(self, investors):
        self.investors = investors

    def set_confidentiality(self, confidentiality):
        self.confidentiality = confidentiality

    def set_cost(self, cost):
        self.cost = cost

    def set_return_on_investment(self, return_on_investment):
        self.return_on_investment = return_on_investment

    def set_customization(self, customization):
        self.customization = customization
