from cpanlp.account.income.revenue import *
from cpanlp.market.commodity import *

class Market:
    def __init__(self,commodity,participants):
        self.commodity = commodity
        self.participants = participants
        self.transaction_costs = None
        self.free_entry=None
        self.number_of_participants = None 
            
def main():
    print("hello")
if __name__ == '__main__':
    main()