import numpy as np
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, Union

#The most important attribute of an asset is its ability to generate cash flow or appreciate in value. This allows the asset to provide a return on investment or to be sold at a profit in the future. Additionally, the reliability and predictability of cash flow and appreciation are also important factors to consider when evaluating an asset.
class Asset:
    """
    #### This class represents a circle with a given radius.

    Attributes:
    debit (float): The radius of the circle.
    account (str): he.
    date (): he

    Methods:
    straight_line_depreciation(): Calculates the area of the circle.
    get_amortization_schedule(): Calculates the circumference of the circle.
    
    Example:
    ```
    circle = Circle(10)
    print(circle.area()) # 314.0
    print(circle.circumference()) # 62.8
    ```
    Learn more about circles in the [official documentation](https://en.wikipedia.org/wiki/Circle).

    """
    accounts = []
    def __init__(self, debit,account = None,date = None):
        self.account = account
        self.debit = debit
        self.date = date
        self.assets=[]
        self.cashflows=[]
        self.is_measurable = True
        self.likely_economic_benefit = True
        self.potential_use=""
        self.market_value =debit
        self.fair_value=None
        self.bubble=self.is_asset_bubble(self.market_value)
        self.target_value = None
        self.uniqueness= None
        Asset.accounts.append(self)
    def __repr__(self):
        return f"Asset({self.account}, {self.debit}, {self.date})"
    def straight_line_depreciation(self,salvage_value, life):
        annual_depreciation = (self.debit - salvage_value) / life
        return annual_depreciation
    def get_amortization_schedule(self,salvage_value, life,rate):
        schedule = []
        annual_depreciation = self.straight_line_depreciation(salvage_value, life)
        for year in range(1, life + 1):
            amortization = self.debit * rate
            depreciation = annual_depreciation
            self.debit -= (amortization + depreciation)
            schedule.append((year, amortization, depreciation))
        return schedule
    def is_asset_bubble(self, price) -> bool:
        return price > (3*self.debit)
    def set_target(self, target_value):
        self.target_value = np.array(target_value)
    def check_target(self):
        if self.target_value is not None:
            if np.all(self.debit > self.target_value):
                print(f"{self.account} has exceeded its target value")
            elif np.all(self.debit < self.target_value):
                print(f"{self.account} has not yet reached its target value")
            else:
                print(f"{self.account} has reached its target value")
        else:
            print(f"{self.account} has no target value set")
    @classmethod
    def withdraw(cls, account, value):
        for equity in Asset.accounts:
            if equity.account == account:
                equity.debit -= value
                break
    @classmethod
    def sum(cls):
        data = [[asset.account, asset.date, asset.debit] for asset in Asset.accounts]
        df = pd.DataFrame(data, columns=['账户类别', '日期', '借方金额'])
        return df
class transaction:
    def __init__(self, item: str, cost: float, quantity: int):
        self.item = item
        self.cost = cost
        self.quantity = quantity
class costaccounting:
    def __init__(self):
        self.transactions = []
    def add_transaction(self, transaction: transaction):
        self.transactions.append(transaction)
    def get_cost(self, item: str) -> float:
        cost = 0
        for transaction in self.transactions:
            if transaction.item == item:
                cost += transaction.cost * transaction.quantity
        return cost
#在会计领域，炒作通常指的是刻意提高某一财务指标或会计概念的价值，以达到获利的目的。这种行为通常会对公司的财务信息的真实性造成负面影响，并可能导致公司遭受监管机构的处罚。在Python中，可以通过定义类来模拟会计概念炒作的情况。例如，可以定义一个名为"AccountingConcept"的类，包括一个名为"manipulate"的方法，用于模拟会计概念炒作的行为    """concept: 会计概念value: 提高的价值
class AccountingConcept:
    def manipulate(self, concept, value):
        pass
class MarketValueManipulation:
  def manipulate(self, asset, value):
      pass
class BalancedScorecard:
      def __init__(self, financial, customer, internal, learning):
            self.financial = financial
            self.customer = customer
            self.internal = internal
            self.learning = learning

#在Python中，可以通过定义类来模拟语法学的情况。例如，可以定义一个名为"Grammar"的类，包含一些属性（例如语言名称、语言类型等）和方法（例如语法分析、句法树构建等）。
def total_asset_value(assets):
    """Calculates the total value of a list of assets."""
    total = 0
    for asset in assets:
        total += asset.debit
    return total
def generate__asset_report(assets):
    """Generates a report with information about a list of assets."""
    report = "ASSET REPORT\n"
    for i in assets:
        report += f"{i.account} ({i.debit}): ${i.date}\n"
    report += f"Total value: ${total_asset_value(assets)}"
    return report
def main():
    a1 = Asset("a1",  100,"2022-01-02")
    a2 = Asset("a2",  200,"2023-01-02")
    a3 = Asset("a3",  300,"2024-01-02")
    Asset.withdraw("a1",30)
    print(Asset.sum())

if __name__ == '__main__':
    main()