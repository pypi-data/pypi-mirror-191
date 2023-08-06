class AdvanceFinancing:
    def __init__(self, borrower, lender, amount, repayment_period, interest_rate):
        self.borrower = borrower
        self.lender = lender
        self.amount = amount
        self.repayment_period = repayment_period
        self.interest_rate = interest_rate
    def set_borrower(self, borrower):
        self.borrower = borrower

    def set_lender(self, lender):
        self.lender = lender

    def set_amount(self, amount):
        self.amount = amount

    def set_repayment_period(self, repayment_period):
        self.repayment_period = repayment_period

    def set_interest_rate(self, interest_rate):
        self.interest_rate = interest_rate
#"垫资"（Advance financing）是指在一方未完成货物或服务的供应前，另一方在同意的条件下提前提供资金的行为。这种方式的资金提供通常是为了帮助另一方完成生产、采购等费用，以保证供货的顺利进行。

#垫资的形式可以是现金或信贷，通常由银行、金融机构或其他金融服务公司提供。垫资的主要目的是为了帮助提高生产效率，提高供货的可靠性，并减少供应链风险。