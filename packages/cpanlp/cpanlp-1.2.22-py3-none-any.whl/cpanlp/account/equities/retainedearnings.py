from cpanlp.account.equities.equity import *
class RetainedEarnings(Equity):
    accounts = []
    def __init__(self, account, credit,date,parties, consideration, obligations,value):
        super().__init__(account, credit,date,parties, consideration, obligations,value)
    @classmethod
    def sum(cls):
        data = [[asset.account, asset.date, asset.credit] for asset in RetainedEarnings.accounts]
        df = pd.DataFrame(data, columns=['账户类别', '日期', '贷方金额'])
        return df