from cpanlp.account.equities.equity import *

#"Equity" and "share" are often used interchangeably to refer to ownership in a company represented by a unit of stock. They both refer to the same concept, but "equity" is a more general term that can refer to other forms of ownership as well, such as ownership in a partnership or real estate.

#In the context of a publicly traded company, equity typically refers to the value of the company's assets minus its liabilities, and a share represents a unit of that equity. When you own shares in a company, you own a portion of the company's equity and are entitled to a portion of its profits and assets.

#In summary, "equity" is a broader term that can refer to different forms of ownership, while "share" specifically refers to a unit of stock representing ownership in a company.

class Share(Equity):
    Account=[]
    def __init__(self, account, shares,price=None,credit=None,date=None,parties=None, consideration=None, obligations=None,value=None):
        super().__init__( account, credit,date,parties, consideration, obligations,value)
        self.shares = shares
        self.price= price
        Share.accounts.append(self)
class PledgedShare(Share):
    Account=[]
    def __init__(self, pledge_date,account, shares,price,credit,date,parties, consideration, obligations,value):
        super().__init__(account, shares,price,credit,date,parties, consideration, obligations,value)
        self.pledge_date = pledge_date
        PledgedShare.accounts.append(self)
class FrozenShare(Share):
    Account=[]
    def __init__(self, freeze_date,account, shares,price,credit,date,parties, consideration, obligations,value):
        super().__init__(account, shares,price,credit,date,parties, consideration, obligations,value)
        self.freeze_date = freeze_date
        FrozenShare.accounts.append(self)