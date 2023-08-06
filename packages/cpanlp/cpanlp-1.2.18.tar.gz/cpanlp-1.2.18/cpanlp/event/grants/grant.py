class Grant:
    def __init__(self, recipient=None, donor=None, amount=None, purpose=None, deadline=None):
        self.recipient = recipient
        self.donor = donor
        self.amount = amount
        self.purpose = purpose
        self.deadline = deadline

    def set_recipient(self, recipient):
        self.recipient = recipient

    def set_donor(self, donor):
        self.donor = donor

    def set_amount(self, amount):
        self.amount = amount

    def set_purpose(self, purpose):
        self.purpose = purpose

    def set_deadline(self, deadline):
        self.deadline = deadline
