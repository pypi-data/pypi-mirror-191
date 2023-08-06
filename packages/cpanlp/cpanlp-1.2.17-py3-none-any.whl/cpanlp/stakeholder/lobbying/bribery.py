from cpanlp.stakeholder.lobbying.lobbying import *
class Bribery(Lobbying):
    def __init__(self, name, company=None, interest_group=None, favor=None,target=None,bribes=None,legality=False,secretive=True,undue_influence=True,direct=None):
        super().__init__(name, company, interest_group, target)
        self.legality=legality
        self.secretive=secretive
        self.favor=favor
        self.undue_influence=undue_influence
        self.bribes=bribes
        self.direct=direct