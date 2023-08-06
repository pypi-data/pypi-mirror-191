from cpanlp.information.information import *

class SpeculativeInformation(Information):
    def __init__(self, message, accuracy, likelihood):
        super().__init__(message)
        self.accuracy = accuracy
        self.likelihood = likelihood
    @property
    def assess_value(self):
        return self.value * self.accuracy * self.likelihood
            