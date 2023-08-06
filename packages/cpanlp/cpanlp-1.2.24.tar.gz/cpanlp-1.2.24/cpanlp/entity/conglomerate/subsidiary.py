from cpanlp.entity.LLC import *


class Subsidiary(LLC):
    def __init__(self, name,type,capital, parent_company):
        super().__init__(name,type,capital)
        self.parent_company = parent_company
        self.is_wholly_owned =None