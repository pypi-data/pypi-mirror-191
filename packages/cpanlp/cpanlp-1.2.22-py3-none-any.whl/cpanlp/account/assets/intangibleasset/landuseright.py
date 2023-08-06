from cpanlp.account.assets.intangibleasset.intangibleasset import *

class LandUseRight(IntangibleAsset):
    def __init__(self, account,debit, date,amortization_rate, land_location):
        super().__init__(account,debit, date,amortization_rate)
        self.land_location = land_location