from cpanlp.entity.LLC import *


class JointVenture(LLC):
    def __init__(self, name,type,capital, partners, project):
        super().__init__(name,type,capital)
        self.partners = partners
        self.project = project
