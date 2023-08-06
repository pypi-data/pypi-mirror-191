from cpanlp.account.assets.intangibleasset.intangibleasset import *

class Goodwill(IntangibleAsset):
    def __init__(self,account,debit, date,amortization_rate):
        super().__init__(account,debit, date,amortization_rate)
        
def main():
    c=Goodwill("a",3000,"2022-01-01",0.3)
    print(c.debit)

if __name__ == '__main__':
    main()
