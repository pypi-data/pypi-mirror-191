class BonusIssue:
    def __init__(self, company, shares_before, shares_after, stock_price):
        self.company = company
        self.shares_before = shares_before
        self.shares_after = shares_after
        self.stock_price = stock_price

    def set_company(self, company):
        self.company = company

    def set_shares_before(self, shares_before):
        self.shares_before = shares_before

    def set_shares_after(self, shares_after):
        self.shares_after = shares_after

    def set_stock_price(self, stock_price):
        self.stock_price = stock_price

    def calculate_increase_in_shares(self):
        return self.shares_after - self.shares_before

    def calculate_increase_in_stock_price(self):
        return (self.stock_price * self.shares_after) / self.shares_before
