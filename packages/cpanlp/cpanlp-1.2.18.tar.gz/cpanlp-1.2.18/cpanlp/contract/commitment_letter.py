from cpanlp.contract.contract import *

class CommitmentLetter(Contract):
    def __init__(self,commitment=None, buyer=None, seller=None, stock_symbol=None, price=None, quantity=None, date=None,parties=None, consideration=None,obligations=None):
        super().__init__(parties, consideration,obligations)
        self.commitment = commitment
        self.buyer = buyer
        self.seller = seller
        self.stock_symbol = stock_symbol
        self.price = price
        self.quantity = quantity
        self.date = date

    def set_buyer(self, buyer):
        self.buyer = buyer

    def set_seller(self, seller):
        self.seller = seller

    def set_stock_symbol(self, stock_symbol):
        self.stock_symbol = stock_symbol

    def set_price(self, price):
        self.price = price

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_date(self, date):
        self.date = date
#承诺函是属于合同的一种。承诺函" 是证券市场上的一种文件，是由股票买方和卖方签署的协议，承诺在未来某一时间内完成股票交易。承诺函通常是在证券市场上进行股票买卖交易的一种常用方式。

#承诺函通常包括交易的详细信息，如交易价格、交易数量、交易日期等。在签署承诺函之后，买方和卖方均有义务遵守协议，在协议规定的日期内完成交易。如果一方未能遵守协议，可能会导致资金损失或法律责任。

#因此，在签署承诺函之前，投资者应该仔细评估市场状况，以确保交易是合理的。此外，投资者应该与法律顾问合作，以确保承诺函的合法性和有效性。