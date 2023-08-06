class Repurchase:
    def __init__(self, company, repurchase_price, repurchase_quantity,stock_symbol=None,buget=None,price_limit=None,financing_method=None,trading_method=None,purpose=None):
        self.company = company
        self.stock_symbol = stock_symbol
        self.repurchase_price = repurchase_price
        self.repurchase_quantity = repurchase_quantity
        self.total_cost = self.repurchase_price * self.repurchase_quantity
        self.buget=buget
        self.price_limit = price_limit
        self.purpose = purpose
        self.financing_method = financing_method
        self.trading_method = trading_method