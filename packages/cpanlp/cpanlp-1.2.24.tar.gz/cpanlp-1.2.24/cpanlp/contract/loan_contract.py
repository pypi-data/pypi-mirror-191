from cpanlp.contract.contract import *
class LoanContract(Contract):
    accounts = []
    #The basic agreement in a labor contract is: B will do what A asks him to do for the term of the contract, in return for a given salary.
    def __init__(self, parties=None,  consideration=None,obligations=None, interest_rate=None):
        super().__init__(parties, consideration,obligations)
        self.interest_rate = interest_rate
        self.repayment_terms =None
        self.collateral = None
        self.prepayment = None
        self.amortization_schedule = []
        self.insurance = None
        LoanContract.accounts.append(self)
    def calculate_amortization(self):
        remaining_balance = self.consideration
        current_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        interest = self.interest_payment(self.start_date)
        while current_date <= end_date:
            principal = self.consideration * self.interest_rate / (1 - (1 + self.interest_rate) ** -(end_date - current_date).days)
            remaining_balance -= principal
            self.amortization_schedule.append({"date": current_date, "interest": interest, "principal": principal, "remaining_balance": remaining_balance})
            current_date += timedelta(days=30)
    def interest_payment(self, date):
        end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()
        start_date = datetime.strptime(date, "%Y-%m-%d").date()
        interest = (self.consideration * self.interest_rate * (end_date -start_date).days) / 365
        return interest
    def principal_payment(self, date):
        principal = 0
        for payment in self.amortization_schedule:
            if payment["date"] == date:
                principal = payment["principal"]
                break
        return principal