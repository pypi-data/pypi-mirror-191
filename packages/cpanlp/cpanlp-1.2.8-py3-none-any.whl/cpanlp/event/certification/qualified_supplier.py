from cpanlp.event.certification.certification import *

class QualifiedSupplierCertification(Certification):
    def __init__(self, supplier_name,name,date_obtained=None,valid_until=None):
        super().__init__(name, date_obtained,valid_until)
        self.supplier_name = supplier_name
        self.certification_obtained = False
        
    def obtain_certification(self):
        # logic to obtain certification, check criteria and requirements
        self.certification_obtained = True
        print(f"{self.supplier_name} has obtained the Qualified Supplier Certification.")
    @property    
    def is_certified(self):
        return self.certification_obtained