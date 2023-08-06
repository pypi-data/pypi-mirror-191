from cpanlp.contract.financial_instrument.financial_instrument import *
import numpy as np
from scipy import stats
class Option(FinancialInstrument):
    def __init__(self, stock_price, strike_price, risk_free_rate, time_to_maturity, volatility,parties=None, consideration=None,obligations=None, value=None):
        super().__init__(parties, consideration,obligations, value)
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.risk_free_rate = risk_free_rate
        self.time_to_maturity = time_to_maturity
        self.volatility = volatility

    def call_price(self):
        d1 = (np.log(self.stock_price / self.strike_price) + (self.risk_free_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity) / (self.volatility * np.sqrt(self.time_to_maturity))
        d2 = d1 - self.volatility * np.sqrt(self.time_to_maturity)
        call_price = self.stock_price * stats.norm.cdf(d1) - self.strike_price * np.exp(-self.risk_free_rate * self.time_to_maturity) * stats.norm.cdf(d2)
        return call_price

    def put_price(self):
        d1 = (np.log(self.stock_price / self.strike_price) + (self.risk_free_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity) / (self.volatility * np.sqrt(self.time_to_maturity))
        d2 = d1 - self.volatility * np.sqrt(self.time_to_maturity)
        put_price = self.strike_price * np.exp(-self.risk_free_rate * self.time_to_maturity) * stats.norm.cdf(-d2) - self.stock_price * stats.norm.cdf(-d1)
        return put_price
#例如股票价格、履约价格、无风险利率、到期时间和波动率。

#然后，我们实现了两个函数 call_price 和 put_price，用于计算认购期权和认沽期权的价格


