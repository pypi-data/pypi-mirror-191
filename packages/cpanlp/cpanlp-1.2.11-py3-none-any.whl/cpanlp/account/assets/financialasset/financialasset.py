from cpanlp.contract.financial_instrument.financial_instrument import *
from cpanlp.account.assets.asset import *
import numpy as np
class FinancialAsset(Asset,FinancialInstrument):
     accounts = []
     def __init__(self, account, debit,date,parties, consideration, obligations,value):
         Asset.__init__(self, account, debit,date)
         FinancialInstrument.__init__(self,parties, consideration,obligations, value)
         self.accumulated_impairment = 0
         self.market_values = None
         self.investment_return = 0
         self.cash_flow = 0
         self.cash_flows=np.array(0)
         FinancialAsset.accounts.append(self)
         
     @property
     def impairment(self):
            # 假设减值准备的计算方式为财务资产的净值减去其市场价值
         net_value = self.debit  # 假设财务资产的净值为其当前价值
         impairment = net_value - self.market_value
         if impairment > 0:
             self.accumulated_impairment += impairment
     def __str__(self):
         return f"{self.account}: {self.debit} (Accumulated Impairment: {self.accumulated_impairment})"
     @property
     def roi(self):
         return (self.value - self.debit) / self.debit
     @property
     def cfar(self):
         cfar = (self.investment_return/self.cash_flow) * np.std(self.cash_flows)
         return cfar
     def plot_market_trend(self):
            plt.plot(self.market_values)
            plt.xlabel('time')
            plt.ylabel('price')
            plt.title(f'{self.account} market trend')
            plt.show()
#计提减值准备是指企业在报告期内根据财务报表计算，为了体现财务资产减值而发生的费用。减值准备通常是在财务资产出现损失时进行计提。
def main():
    a=FinancialAsset("stock",100,"2022-01-02","gup",3000,"持有",100)
    print(a.roi)
    print(FinancialAsset.accounts)
if __name__ == '__main__':
    main()