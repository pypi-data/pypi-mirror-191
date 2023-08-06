class Tax:
    def __init__(self, rate, base,deductions):
        self.rate = rate
        self.base = base
        self.deductions =deductions
        self.object=None
        self.payer=None
        self.incentives=None
        self.deadline=None
        self.location=None
        self.history = []
       
class TurnoverTax(Tax):
    def __init__(self, rate, base,deductions):
        super().__init__(rate, base,deductions)
class VAT(TurnoverTax):
    def __init__(self, rate, base,deductions):
        super().__init__(rate, base,deductions)
class ConsumptionTax(TurnoverTax):
    def __init__(self, rate, base,deductions):
        super().__init__(rate, base,deductions)
class IncomeTax(Tax):
    def __init__(self, rate, base, deductions):
        super().__init__(rate, base,deductions)
    def calculate(self, income):
        taxable_income = income - self.deductions
        return taxable_income * self.rate + self.base       
class PersonalIncomeTax(IncomeTax):
    def __init__(self, rate, base, deductions, exemptions):
        super().__init__(rate, base, deductions)
        self.exemptions = exemptions
class CorporateIncomeTax(IncomeTax):
    def __init__(self, rate, base, deductions, exemptions):
        super().__init__(rate, base, deductions)
        self.exemptions = exemptions
        
class PropertyTax(Tax):
    def __init__(self, rate, base,deductions,value):
        super().__init__(rate, base,deductions)
        self.value = value
    @property
    def tax(self):
        return self.value * self.rate
class RealEstateTax(PropertyTax):
    def __init__(self, rate, base,deductions,value, square_footage):
        super().__init__(rate, base,deductions,value)
        self.square_footage = square_footage
    @property
    def tax(self):
        base_tax = super().calculate_tax()
        return base_tax + (self.square_footage * 0.05)
class BehaviorTax(Tax):
    def __init__(self, rate, base,deductions,amount):
        super().__init__(rate, base,deductions)
        self.amount = amount
    @property
    def tax(self):
        return self.amount * self.rate
class TransactionTax(BehaviorTax):
    def __init__(self, rate, base,deductions,amount, transaction):
        super().__init__(rate, base,deductions,amount)
        self.transaction = transaction
    @property
    def tax(self):
        base_tax = super().calculate_tax()
        return base_tax + (self.transaction * 0.05)
def main():
    income = 1000
    vat = IncomeTax(0.1,200,20)
    print(vat.calculate(income))
if __name__ == '__main__':
    main()
