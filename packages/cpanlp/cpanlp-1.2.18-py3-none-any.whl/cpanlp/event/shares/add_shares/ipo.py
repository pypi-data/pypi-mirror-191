class IPO:
    def __init__(self, company, stock_symbol, stock_price, shares_offered, underwriters):
        self.company = company
        self.stock_symbol = stock_symbol
        self.stock_price = stock_price
        self.shares_offered = shares_offered
        self.underwriters = underwriters

    def set_company(self, company):
        self.company = company

    def set_stock_symbol(self, stock_symbol):
        self.stock_symbol = stock_symbol

    def set_stock_price(self, stock_price):
        self.stock_price = stock_price

    def set_shares_offered(self, shares_offered):
        self.shares_offered = shares_offered

    def set_underwriters(self, underwriters):
        self.underwriters = underwriters
