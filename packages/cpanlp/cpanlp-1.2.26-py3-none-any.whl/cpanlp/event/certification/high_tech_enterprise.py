from cpanlp.event.certification.certification import *
class HighTechEnterpriseCertification(Certification):
    def __init__(self, name, RD_expenditure=None, patent_count=None, revenue=None,date_obtained=None,valid_until=None):
        super().__init__(name, date_obtained,valid_until)
        self.RD_expenditure = RD_expenditure
        self.patent_count = patent_count
        self.revenue = revenue
    
    def is_qualified(self):
        if self.RD_expenditure / self.revenue >= 0.1 and self.patent_count >= 5:
            return True
        else:
            return False
    
    def get_status(self):
        if self.is_qualified():
            return f"{self.name} is certified as a Hi-Tech Enterprise."
        else:
            return f"{self.name} does not meet the criteria for Hi-Tech Enterprise certification."
