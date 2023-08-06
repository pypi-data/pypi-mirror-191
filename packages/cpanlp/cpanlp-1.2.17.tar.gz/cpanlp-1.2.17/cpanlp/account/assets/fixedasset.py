from cpanlp.account.assets.asset import *
from collections import namedtuple
Costs = namedtuple('Costs', ('purchase_price', 'taxes', 'transportation_costs', 'installation_costs', 'professional_services_costs'))

#The most important attribute of a fixed asset is its ability to generate revenue or savings for the company. This can be through the asset's use in the production of goods or services, or through cost savings from the asset's use. Other important attributes of fixed assets include durability, reliability, and maintainability, as well as the asset's ability to retain its value over time. Additionally, factors such as the asset's useful life, as well as the company's ability to effectively utilize the asset, are also important to consider when evaluating a fixed asset.
class FixedAsset(Asset):
    accounts = []
    def __init__(self, account,debit,date,costs,life_span,location):
        super().__init__(account, debit, date)
        self.location=location
        self.costs= costs
        if life_span < 1:
            raise ValueError("Value must be between 0 and 1")
        self.life_span = life_span
        self.depreciation_history = []
        self.age = 0.0
        self.is_leased=False
        self.maintainability=True
        self.status = None
        self.depreciation_method=None
        self.cost_savings = None
        FixedAsset.accounts.append(self)
    def __str__(self):
        return f"{self.account} ({self.debit}), Location: {self.location}"
    def depreciate(self, rate):
        if rate < 0 or rate > 1:
            raise ValueError("Value must be between 0 and 1")
        if self.age < self.life_span:
            self.depreciation_history.append(rate*self.debit)
            a = rate*self.debit
            self.debit -= a
            self.age += 1
        else:
            print("Asset already reach its life span,no more depreciation.")
    def total_cost(self):
        return sum(self.costs)
    @classmethod
    def withdraw(cls, account, value):
        for equity in FixedAsset.accounts:
            if equity.account == account:
                equity.debit -= value
                break
    @classmethod
    def sum(cls):
        data = [[asset1.account, asset1.date, asset1.debit] for asset1 in FixedAsset.accounts]
        df = pd.DataFrame(data, columns=['账户类别', '日期', '借方金额'])
        return df
class Land(Asset):
    accounts = []
    def __init__(self,account, debit, date,area,market_value):
        super().__init__(account, debit, date)
        self.area=area
        self.market_value=market_value
        Land.accounts.append(self)
    def zoning(self):
        # method to check zoning of land
        pass
    def rental_income(self, rental_rate):
        return self.area * rental_rate
    def appreciation(self):
        return self.market_value - self.debit
    def encumbrances(self):
        # method to check if the land has any encumbrances like mortgages, liens, etc
        pass
class RealState(FixedAsset):
    pass
def main():
    a12=FixedAsset("zhang1",11500,"2022-02-21",Costs(purchase_price=1000, taxes=100,transportation_costs=200, installation_costs=300, professional_services_costs=400),5,"beijing")
    print(a12.debit)
    print(a12.location)
    print(a12.likely_economic_benefit)
    a22=FixedAsset("zhang1",11500,"2022-02-21",Costs(purchase_price=1000, taxes=100,transportation_costs=200, installation_costs=300, professional_services_costs=400),5,"beijing")
    a22.depreciate(0.2)
    print(a22.depreciation_history)
    print(FixedAsset.sum())
if __name__ == '__main__':
    main()