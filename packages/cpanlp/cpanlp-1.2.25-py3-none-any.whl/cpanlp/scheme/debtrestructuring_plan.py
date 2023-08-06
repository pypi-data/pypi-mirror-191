class DebtRestructuringPlan:
    def __init__(self, name, amount, terms, creditors):
        self.name = name
        self.amount = amount
        self.terms = terms
        self.creditors = creditors
        
    def display_info(self):
        # Display information about the debt restructuring plan
        print("Debt Restructuring Plan:", self.name)
        print("Amount:", self.amount)
        print("Terms:", self.terms)
        print("Creditors:", self.creditors)
        
    def update_terms(self, new_terms):
        # Update the terms of the debt restructuring plan
        self.terms = new_terms
        
    def add_creditor(self, creditor):
        # Add a creditor to the list of creditors
        self.creditors.append(creditor)
        
    def remove_creditor(self, creditor):
        # Remove a creditor from the list of creditors
        self.creditors.remove(creditor)
