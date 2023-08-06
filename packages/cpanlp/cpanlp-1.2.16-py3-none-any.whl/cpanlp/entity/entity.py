from typing import List
from cpanlp.account.assets.asset import *
from cpanlp.market.market import *

class LegalEntity:
    def __init__(self, name, type=None,capital=None):
        self.name = name
        self.type = type
        self.registration_number=""
        self.address=""
        self.capital=capital
        self.employees =[]
        self.assets=[]
        self.partners = []
        self.departments = []
        self.agency_cost = None
        self.market_leader = False
        self.market_share = None
        self.sales =None
        self.asset = None
        self.liability = 0.0    
        self.investment = 0.0
        self.revenue = None
        self.business_scope = None
        self.registered_capital = 0.0
        self.shareholders = None
        self.legal_representative = None
        self.is_bankrupt = False
    def add_department(self, department):
        self.departments.append(department)
    def add_partner(self, partner):
        self.partners.append(partner)
    def fire_employee(self, employee):
        self.employees.remove(employee)
    def hire_employee(self, employee):
        self.employees.append(employee)
    def totalsalary(self):
        return 0.0 if self.employees is None else sum([member.salary for member in self.employees])
    def merge(self, other_entity):
        """
        Merges the current LLC with another LLC
        """
        # Logic to merge the two LLCs
        self.employees.extend(other_entity.employees)
        self.capital += other_entity.capital
        self.name = f"{self.name}-{other_entity.name}"
    def spin_off(self, spin_off_name:str,spin_off_type:str,spin_off_capital:float):
        """
        Creates a new LLC as a spin-off of the current LLC
        """
        return LegalEntity(spin_off_name,spin_off_type,spin_off_capital)
    def increase_capital(self, amount):
        """
        Increases the capital of the LLC
        """
        self.capital += amount
    def decrease_capital(self, amount):
        """
        Decreases the capital of the LLC
        """
        if self.capital - amount < 0:
            raise ValueError("Capital can not be negative")
        self.capital -= amount
    def enter_market(self, market:Market):
        return market
    
def main():
    a=LegalEntity("zhang")
    print(a.name)
if __name__ == '__main__':
    main()