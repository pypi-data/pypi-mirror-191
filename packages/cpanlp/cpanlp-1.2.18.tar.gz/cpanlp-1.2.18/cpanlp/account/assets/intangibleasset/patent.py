from cpanlp.account.assets.intangibleasset.intangibleasset import *

class Patent(IntangibleAsset):
    def __init__(self, name=None,inventor=None, patent_type=None,account=None,debit=None, date=None,amortization_rate=None,patent_number=None, application_date=None, announcement_number=None, certificate_number=None):
        super().__init__(account,debit, date,amortization_rate)
        self.patent_number = patent_number
        self.application_date = application_date
        self.announcement_number = announcement_number
        self.certificate_number = certificate_number
        self.name=name
        
    def __str__(self):
        return "Patent: Name - {}, Patent number - {}, Application date - {}, Announcement number - {}, Certificate number - {}".format(
            self.name, self.patent_number, self.application_date, self.announcement_number, self.certificate_number
        )
        
    def is_valid(self):
        print("The patent is still valid.")
def main():
    utility_patent = Patent(name="A new method for producing electricity", inventor="John Doe", patent_type="Utility Patent")
#Utility Patent- Issued for the invention of a new and useful process, machine, manufacture, or composition of matter, or a new and useful improvement thereof
if __name__ == '__main__':
    main()