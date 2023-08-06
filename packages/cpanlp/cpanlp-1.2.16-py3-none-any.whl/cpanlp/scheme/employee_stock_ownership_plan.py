from datetime import datetime

class EmployeeStockOwnershipPlan:
    def __init__(self, employee_id, stock_symbol, shares_granted, grant_date, vesting_period, vesting_cliff):
        self.employee_id = employee_id
        self.stock_symbol = stock_symbol
        self.shares_granted = shares_granted
        self.grant_date= datetime.strptime(grant_date, "%Y-%m-%d").date()
        self.vesting_period = vesting_period
        self.vesting_cliff = vesting_cliff
        
    def vest_shares(self, current_date):
        time_elapsed = (datetime.strptime(current_date, "%Y-%m-%d").date() - self.grant_date).days
        if time_elapsed < self.vesting_cliff:
            return 0
        else:
            vested_shares = self.shares_granted * ((time_elapsed - self.vesting_cliff) / self.vesting_period)
            return min(vested_shares, self.shares_granted)