from cpanlp.market.goods import *

class Sale(Goods):
    """
    ### ChatGPT:
    Revenue 指的是公司在一定时期内从销售商品或提供服务中获得的收入。它是在销售过程中产生的收入，不包括其它来源的收入。
    Income 指的是公司在一定时期内所有来源的收入总和。除了销售收入，还包括其它来源的收入，如投资收益、利息收入、租金收入等。
    revenue 是 income 的一部分，但是 income 不一定包括 revenue。简单来说，Revenue 是指销售收入，而 Income 是指
    """
    accounts = []
    def __init__(self, quarter=None, amount=None, amount_unit=None,growth_rate=None, segment=None,year=None,customer=None,goods=None, fair_value=None,market_price=None, supply=None, demand=None, quantity=None, unit_price=None,date=None,year_on_year=None,quarter_on_quarter=None,month_on_month=None):
        super().__init__(goods, fair_value,market_price, supply, demand)
        self.quarter=quarter
        self.customer=customer
        self.quantity = quantity
        self.unit_price = unit_price
        self.date=date
        self.supply_curve = {1:3,1:4}
        self.demand_curve = {1:3,1:4}
        self.accuracy= None
        self.completeness = None
        self.validity = None
        self.growth_rate =growth_rate
        self.year = year
        self.amount = amount
        self.amount_unit =amount_unit
        self.segment= segment
        self.year_on_year = year_on_year
        self.quarter_on_quarter =quarter_on_quarter
        self.month_on_month = month_on_month
        Sale.accounts.append(self)
class NetSales:
    def __init__(self, amount, growth_rate, forex_impact):
        self.amount = amount
        self.growth_rate = growth_rate
        self.forex_impact = forex_impact
   


