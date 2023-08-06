
from cpanlp.culture.spirit.spirit import *
from cpanlp.utility.utility import *
from scipy.optimize import minimize
import math
import numpy as np
import pandas as pd
def calculate_beta(portfolio):
    # Load historical data for each stock in the portfolio
    stocks_data = {}
    for stock in portfolio:
        data = pd.read_csv(stock + ".csv")
        stocks_data[stock] = data
    # Calculate the daily returns for each stock
    returns = {}
    for stock, data in stocks_data.items():
        returns[stock] = data["Adj Close"].pct_change()
    # Calculate the covariance matrix between the returns of all stocks
    cov_matrix = np.cov(list(returns.values()))
    # Calculate the beta value of the portfolio
    beta = cov_matrix[0][1] / np.var(returns["market"])
    return beta
class Consumer:
    def __init__(self, name, age=None,wealth=None, utility_function=None):
        self.name = name
        self.age = age
        self.wealth= wealth
        self.commodity_prices=[]
        self.utility_function = utility_function
    def calculate_utility(self, goods, prices, income):
        """
        Calculates the total utility for a consumer given a set of goods, their prices, and the consumer's income
        """
        total_utility = 0
        for i in range(len(goods)):
            total_utility += math.log(np.log(goods[i]) - prices[i] / self.wealth)
        return total_utility
    def indifference_curve(self, x):
        # Indifference curve function
        # U(x1,x2) = sqrt(x1) + sqrt(x2)
        # Budget constraint: p1*x1 + p2*x2 <= income
        U=self.utility_function
        return U(x[0]) + U(x[1])
    def budget_constraint(self, x):
        p1, p2 = self.commodity_prices
        return p1 * x[0] + p2 * x[1] - self.wealth
    def optimize_utility(self,prices):
        self.commodity_prices=prices
        x0 = [2, 2]
        bounds=[[0,None],[0,None]]
        constraints = {'type': 'ineq', 'fun': self.budget_constraint}
        res = minimize(self.indifference_curve, x0, bounds=bounds,constraints=constraints)
        return res.x
def main():
    U= CRRA(0.8)
    lucy = Consumer("lucy",23,1000,U.utility)
    print(lucy.optimize_utility([110, 20]))
if __name__ == '__main__':
    main()