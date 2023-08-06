from cpanlp.account.assets.intangibleasset.intangibleasset import *

class Franchise(IntangibleAsset):
    """
    ### ChatGPT:
    Franchise rights（特许经营权）是指一种商业模式，授权企业向授权人提供商业模式、品牌、产品、技术、管理支持等资源，以获得特许经营权使用费和一定的利润分成。授权人通常需要遵循特定的规则和程序，并支付一定的费用。
    
    Franchise rights的特征包括：
    
    品牌共享：授权人使用特许经营权人的品牌、商标、专利等资源，以提高品牌知名度和市场占有率。
    经营模式标准化：特许经营权人提供标准化的经营模式、产品、服务等，使得授权人可以更容易地开展业务，并提高效率和利润。
    管理支持：特许经营权人提供包括培训、市场营销、技术支持等在内的全面的管理支持，以确保授权人的业务能够成功。
    费用支付：授权人需要向特许经营权人支付一定的授权费、管理费等，以获得使用特许经营权的权利。
       
    """
    def __init__(self, brand=None, products=None, services=None, training=None, marketing=None, support=None,account=None,debit=None, date=None,amortization_rate=None):
        super().__init__(account,debit, date,amortization_rate)

        self.brand = brand # 品牌
        self.products = products # 产品
        self.services = services # 服务
        self.training = training # 培训
        self.marketing = marketing # 市场营销
        self.support = support # 技术支持

    def provide_brand(self):
        # 提供品牌共享
        pass

    def standardize_operations(self):
        # 经营模式标准化
        pass

    def provide_support(self):
        # 提供全面的管理支持
        pass

    def collect_fees(self):
        # 收取授权费、管理费等
        pass
