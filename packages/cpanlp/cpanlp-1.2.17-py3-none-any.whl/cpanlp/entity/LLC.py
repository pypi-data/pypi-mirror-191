from cpanlp.entity.incorporate import *
from datetime import timedelta, date
import random
class LLC(IncorporatedEntity):
    def __init__(self, name,type=None,capital=None):
        super().__init__(name,type,capital)
        self.goods = []
        self.monopoly = False
        self.monopoly_start = None
        self.monopoly_end = None
        self.subsidiaries = []
        self.ownership = None
        self.control = None
        self.shareholders = []
        self.board_members = []
        self.board_of_supervisors = []
        self.independent_financial_advisor = None
        self.chairman = None
        self.main_business = None
        self.previous_main_business = None
    @property
    def main_business_has_changed(self):
        return self.main_business != self.previous_main_business

    def establish_subsidiary(self, subsidiary_name, subsidiary_type, subsidiary_capital):
        """
        Create a new subsidiary LLC 
        """
        subsidiary = LLC(subsidiary_name, subsidiary_type,subsidiary_capital)
        self.subsidiaries.append(subsidiary)
        return subsidiary
    def transfer_assets(self, subsidiary, assets):
        """
        Transfer assets to subsidiary
        """
        if subsidiary not in self.subsidiaries:
            raise ValueError(f"{subsidiary.name} is not a subsidiary of {self.name}")
        for asset in assets:
            if asset not in self.assets:
                raise ValueError(f"{asset} is not an asset of {self.name}")
            self.assets.remove(asset)
            subsidiary.assets.append(asset)
        return f"Assets {assets} are transferred to {subsidiary.name} successfully"
    def innovate(self,new_goods):
        # simulate the innovation process
        self.new_good = new_goods
        self.goods.append(new_goods)
        self.monopoly = True
        self.monopoly_start = date.today()
        # random number of years for the monopoly to last (between 1 and 5)
        monopoly_years = random.randint(1, 5)
        self.monopoly_end = self.monopoly_start + timedelta(days=365*monopoly_years)
        print(f"{self.name} has innovated and now has a temporary monopoly on {new_goods} until {self.monopoly_end}.")
    def lose_monopoly(self):
        self.monopoly = False
        self.monopoly_start = None
        self.monopoly_end = None
        print(f"{self.name}'s monopoly has ended.")
    def check_monopoly(self):
        if self.monopoly and self.monopoly_end:
            if date.today() > self.monopoly_end:
                self.lose_monopoly()
            else:
                print(f"{self.name} still has a monopoly on {self.goods[-1]} until {self.monopoly_end}.")
        else:
            print(f"{self.name} does not currently have a monopoly.")
    def imitate_product(self, company, product):
        print(f"{self.name} is imitating {product} from {company}.")
        
def main():
    b=LLC("Partner Inc")
    print(b.subsidiaries)
    print("hello")
if __name__ == '__main__':
    main()