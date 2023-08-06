from cpanlp.person.investor.investor import *

class Shareholder(Investor):
    def __init__(self,name,shares=None,expected_return=None, risk_preference=None, portfolio=None,age=None, wealth=None,utility_function=None ):
        super().__init__(name, age, wealth,utility_function,portfolio, expected_return, risk_preference)
        self.shares = shares
        self.restriction = None
    def vote_on_operating_policy(self):
            # shareholder voting on operating policy
        pass
    def vote_on_investment_plan(self):
        # shareholder voting on investment plan
        pass
    def vote_on_board_members(self):
        # shareholder voting on board members
        pass
    def vote_on_compensation(self):
        # shareholder voting on compensation for board members
        pass
    def vote_on_financial_reports(self):
        # shareholder voting on financial reports
        pass
    def vote_on_profit_distribution(self):
        # shareholder voting on profit distribution
        pass
    def vote_on_capital_increase_or_decrease(self):
        # shareholder voting on capital increase or decrease
        pass
    def vote_on_bond_issuance(self):
        # shareholder voting on bond issuance
        pass
    def vote_on_merger_dissolution(self):
        # shareholder voting on merger, dissolution or change of company form
        pass
    def vote_on_amending_articles_of_incorporation(self):
        # shareholder voting on amending articles of incorporation
        pass
def main():
    a=Shareholder("ma")
if __name__ == '__main__':
    main()