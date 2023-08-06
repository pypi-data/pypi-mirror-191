from cpanlp.entity.entity import *
class UnincorporatedEntity(LegalEntity):
    def __init__(self, name, type=None,capital=None):
        super().__init__(name, type,capital)
        self.limited_liability = False
        self.personal_risk = max(self.investment, self.liability)
        self.is_taxed=False
        self.Continuity = "low"
        
class IncorporatedEntity(LegalEntity):
    def __init__(self, name, type=None,capital=None):
        super().__init__(name, type,capital)
        self.limited_liability = True
        self.personal_risk = min(self.investment, self.liability)
        self.is_taxed=True
        self.Continuity = "High"
def main():
    a=UnincorporatedEntity("zhang")
if __name__ == '__main__':
    main()