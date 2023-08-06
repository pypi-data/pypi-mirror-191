from cpanlp.account.assets.intangibleasset.intangibleasset import *

class IntellectualProperty(IntangibleAsset):
    def __init__(self, account,debit, date,amortization_rate, owner):
        super().__init__(account,debit, date,amortization_rate)
        self.owner = owner
    def register_with_government(self):
        print(f"{self.owner} is registered with the government.")