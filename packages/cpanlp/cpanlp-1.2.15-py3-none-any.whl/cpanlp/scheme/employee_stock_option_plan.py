from datetime import datetime
#Employee Stock Ownership Plan (ESOP) and Employee Stock Option Plan (ESOP) are two different forms of employee benefits.

#ESOP (Employee Stock Ownership Plan): An ESOP is a type of defined contribution employee benefit plan in which the employer sets aside a portion of company stock and allocates it to individual employee accounts. ESOPs are designed to provide employees with an ownership interest in the company and to align the interests of employees with those of the company's shareholders.

#ESOP (Employee Stock Option Plan): An ESOP, also known as a stock option plan, is a type of compensation plan in which employees are granted options to purchase company stock at a pre-determined price. ESOPs are designed to incentivize employees and to align their interests with those of the company's shareholders. Employees may exercise their options after a vesting period, which is a set period of time that must elapse before the options become exercisable.


class EmployeeStockOptionPlan:
    def __init__(self, option_grant, option_exercise_price, option_expiration_date):
        self.option_grant = option_grant
        self.option_exercise_price = option_exercise_price
        self.option_expiration_date = datetime.strptime(option_expiration_date, '%Y-%m-%d')
        
    def is_valid(self):
        current_date = datetime.now().date()
        return current_date < self.option_expiration_date
    
    def value(self, current_stock_price):
        if self.is_valid() and current_stock_price > self.option_exercise_price:
            return (current_stock_price - self.option_exercise_price) * self.option_grant
        else:
            return 0