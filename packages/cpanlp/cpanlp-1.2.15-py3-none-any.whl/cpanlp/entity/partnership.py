from cpanlp.entity.incorporate import *

class Partnership(UnincorporatedEntity):
    def __init__(self, name,type=None,capital=None):
        super().__init__(name,type,capital)
        self.partners = []
        self.general_partners = []
        self.limited_partners=[]
    def add_partner(self, partner):
        self.partners.append(partner)
    def remove_partner(self, partner):
        self.partners.remove(partner)
    def distribute_profit(self, profit):
        """Distribute the profit among partners in a pre-agreed ratio."""
        pass
    def voting_procedure(self,proposal):
        """Conduct voting procedure for major decisions on a given proposal"""
        print(f"Proposal: {proposal}")
        for partner in self.partners:
            vote = input(f"{partner}, do you approve this proposal (yes/no)")
            if vote.lower() not in ["yes","no"]:
                print("Invalid input")
            else:
                pass
    def list_partners(self):
        """List all the partners of the partnership"""
        print(self.partners)
        
def main():
    print("hello")
if __name__ == '__main__':
    main()