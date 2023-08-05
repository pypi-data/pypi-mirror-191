from cpanlp.business.business import *

class MainBusiness(Business):
    def __init__(self, name, industry, main_service):
        super().__init__(name, industry)
        self.main_service = main_service

    def description(self):
        return f"{self.name} is a business in the {self.industry} industry. " \
               f"Their main service is {self.main_service}."