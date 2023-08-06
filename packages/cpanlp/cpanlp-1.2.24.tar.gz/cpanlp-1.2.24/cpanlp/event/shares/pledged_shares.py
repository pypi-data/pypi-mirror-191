class PledgedShares:
    def __init__(self, shares,current_price, loan_amount, interest_rate):
        self.current_price =current_price
        self.shares = shares
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.collateral_value = shares * shares.current_price
    
    def loan_repayment(self, term):
        interest = self.loan_amount * self.interest_rate * term
        return self.loan_amount + interest
    
    def update_collateral_value(self, new_price):
        self.collateral_value = self.shares * new_price
        
    def check_collateral(self):
        loan_value = self.loan_amount + self.loan_amount * self.interest_rate
        return self.collateral_value >= loan_value
