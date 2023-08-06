from cpanlp.event.personnel.resignation.resignation import *

class ExecutiveResignation(Resignation):
    def __init__(self, name, reason=None, notice_period=None, final_day=None, severance_package=None):
        super().__init__(name, reason, notice_period, final_day, severance_package)
    def resign(self):
        print(f"Executive {self.name} has resigned due to {self.reason} with a notice period of {self.notice_period} and a severance package of {self.severance_package}.")