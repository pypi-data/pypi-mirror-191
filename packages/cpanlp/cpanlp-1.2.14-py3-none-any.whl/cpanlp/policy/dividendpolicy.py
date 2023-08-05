from cpanlp.policy.policy import *

class DividendPolicy(Policy):
    def __init__(self, name,dividend_rate ,policy_type, purpose):
        super().__init__(name, policy_type, purpose)
        self.dividend_rate = dividend_rate
    
    def set_dividend_rate(self, dividend_rate):
        self.dividend_rate = dividend_rate
        
    def calculate_dividend(self, net_income):
        return net_income * self.dividend_rate
    
def main():
    print(123)
    policy1 = DividendPolicy("Deloitte",0.2,"福利","incentive")
    print(policy1.calculate_dividend(100000)) # prints 7000
if __name__ == '__main__':
    main()