class Environment:
    def __init__(self):
        self.factors = {}
    
    def add_factor(self, factor, value):
        self.factors[factor] = value
    
    def get_factor(self, factor):
        return self.factors.get(factor, None)
    def impact_on_business(self):
        print("The change in the economic environment can impact the sales, costs, and profits of a business.")