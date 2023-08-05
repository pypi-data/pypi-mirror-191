from cpanlp.person.consumer import *

class Investor(Consumer):
    def __init__(self,name, expected_return=None, risk_preference=None,portfolio=None, age=None, wealth=None,utility_function=None):
        super().__init__(name, age,wealth, utility_function)
        self.portfolio = portfolio
        self.expected_return = expected_return
        self.risk_preference = risk_preference
    @property
    def risk_neutrality(self):
        # Code to calculate the beta value of the portfolio
        beta = calculate_beta(self.portfolio)
        return beta
def main():
    print("hello")
if __name__ == '__main__':
    main()