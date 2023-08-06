from cpanlp.contract.financial_instrument.financial_instrument import *
class ConvertibleBond(FinancialInstrument):
    def __init__(self, issuer=None, coupon=None, conversion_price=None, maturity_date=None,parties=None, consideration=None,obligations=None, value=None):
        super().__init__(parties, consideration,obligations, value)
        self.issuer = issuer
        self.coupon = coupon
        self.conversion_price = conversion_price
        self.maturity_date = maturity_date

    def set_issuer(self, issuer):
        self.issuer = issuer

    def set_coupon(self, coupon):
        self.coupon = coupon

    def set_conversion_price(self, conversion_price):
        self.conversion_price = conversion_price

    def set_maturity_date(self, maturity_date):
        self.maturity_date = maturity_date
#ConvertibleBond 类具有四个属性：issuer，coupon，conversion_price 和 maturity_date。这四个属性分别表示发行人、票息、转换价格和到期日。