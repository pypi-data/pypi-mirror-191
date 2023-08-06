from cpanlp.contract.contract import *

class PurchaseContract(Contract):
    def __init__(self, supplier, items, price, parties=None, consideration=None,obligations=None):
        super().__init__(parties, consideration,obligations)
        self.supplier = supplier
        self.items = items
        self.price = price
