from cpanlp.account.assets.asset import *
import random
import matplotlib.pyplot as plt
#The most important attribute of an intangible asset is its ability to generate revenue or create a competitive advantage for the company. Examples of intangible assets include patents, trademarks, copyrights, trade secrets, and brand recognition. Other important attributes include the asset's uniqueness, its ability to be protected legally, and the duration of its useful life. Additionally, the company's ability to effectively utilize the asset to generate revenue or create a competitive advantage is also an important factor to consider when evaluating an intangible asset.
class IntangibleAsset(Asset):
    accounts = []
    def __init__(self,account,debit, date,amortization_rate):
        super().__init__(account, debit, date)
        if amortization_rate < 0 or amortization_rate > 1:
            raise ValueError("amortization_rate must be between 0 and 1")
        self.amortization_rate = amortization_rate
        self.amortization_history = []
        self.market_value = None
        self.competitive_advantage=None
        self.is_separable=True
        self.has_physical_substance=False
        self.non_monetary = True
        IntangibleAsset.accounts.append(self)
    def train(self):
        pass
    def predict(self, num_steps):
        pass
    def amortize(self):
        self.amortization_history.append(self.amortization_rate*self.debit)
        self.debit -= self.amortization_rate*self.debit
    def simulate_volatility(self, volatility, num_steps):
        prices = [self.debit]
        for i in range(num_steps):
            prices.append(prices[-1] * (1 + volatility * random.uniform(-1, 1)))
        plt.plot(prices)
        plt.show()
    @classmethod
    def withdraw(cls, account, value):
        for equity in IntangibleAsset.accounts:
            if equity.account == account:
                equity.debit -= value
                break
    @classmethod
    def sum(cls):
        data = [[asset1.account, asset1.date, asset1.debit] for asset1 in IntangibleAsset.accounts]
        df = pd.DataFrame(data, columns=['账户类别', '日期', '借方金额'])
        return df
class Happy_New_Year_Asset(IntangibleAsset):
    def __init__(self,account, date,amortization_rate,year_wishes):
        super().__init__(account,0, date,amortization_rate)
        self.year_wishes = year_wishes
        self.debit= len(self.year_wishes)*1000000000000
    def add_wishes(self, wishes):
        self.year_wishes.extend(wishes)
def 新年祝福():
    wishes = ["新年快乐！兔年大吉！", "天天开心，身体健康！", "全家幸福，事事顺心！"]
    happy_asset = Happy_New_Year_Asset("香香","2023-01-22",0.005,wishes)
    happy_asset.add_wishes(wishes)
    happy_asset.amortize(1)
    happy_person = happy_asset.account
    happy_income = happy_asset.amortization_history[0][1]
    print(happy_person,"新年第一天的幸福：",happy_income,"😄") 

def main():
    print(11)
    a=IntangibleAsset("a",3000,"2022-01-01",0.3)
    a.amortize()
    print(IntangibleAsset.sum())
if __name__ == '__main__':
    main()