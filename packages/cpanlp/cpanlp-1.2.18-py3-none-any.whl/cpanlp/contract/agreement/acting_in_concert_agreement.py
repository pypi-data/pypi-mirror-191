from cpanlp.contract.agreement.agreement import *

class ActingInConcertAgreement(Agreement):
    def __init__(self, parties=None, purpose=None, terms=None, consensus_method=None):
        super().__init__(parties, purpose, terms)
        self.consensus_method = consensus_method