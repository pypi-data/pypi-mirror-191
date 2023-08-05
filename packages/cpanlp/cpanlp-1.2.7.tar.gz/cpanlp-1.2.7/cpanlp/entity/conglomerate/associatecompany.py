from cpanlp.entity.LLC import *

class AssociateCompany(LLC):
    def __init__(self, name,type,capital, parent_company):
        super().__init__(name,type,capital)
        self.parent_company = parent_company

#Joint venture公司和 associate 公司是在商业和企业管理中常用的术语。Joint venture 公司是指两个或多个公司共同创建一个新公司，并共同拥有和管理该公司。这种公司通常是为了完成特定的项目或业务而设立的。双方公司会共同承担风险和收益。Associate 公司是指一家公司持有另一家公司的股权，但并不控制该公司的经营管理。 Associate 公司可以是一家独立的公司，也可以是一家子公司。与 Joint venture公司相比，Associate 公司的风险和收益主要由持股公司承担。总的来说，Joint venture 公司是双方公司共同创建和管理的公司，而 Associate 公司是一家公司持有另一家公司的股权，但不控制其经营管理。