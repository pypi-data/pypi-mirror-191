class Certification:
    def __init__(self, name, date_obtained=None,valid_until=None):
        self.name = name
        self.date_obtained = date_obtained
        self.valid_until = valid_until
    @property
    def is_valid(self):
        """Returns True if the certification is still valid, False otherwise"""
        return self.date_obtained is not None