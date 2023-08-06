from cpanlp.stakeholder.fund.fundcompany import *

class PrivateFund(FundCompany):
    def __init__(self,name=None, investment_strategy=None, type=None,capital=None, interests=None,power=None):
        super().__init__(name, investment_strategy, type,capital, interests,power)
def main():
    private_fund = PrivateFund(name="ABC Private Fund", investment_strategy="Long-term equity investing")
    print(private_fund.investment_strategy)
if __name__ == '__main__':
    main()
