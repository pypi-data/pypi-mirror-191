from cpanlp.economic_system.economic_system import *

class FinancialSystem(EconomicSystem):
    """
    ### ChatGPT:
    
    经济系统（economic system）是指一个国家或地区用来生产、分配和消费有限资源的一系列制度、机构和行为。金融体系（financial system）是经济系统的一个组成部分，它由银行、金融市场、保险公司、证券公司等金融机构和相关市场组成，提供融资、支付、风险管理、信息传递等金融服务。

    因此，金融体系是经济系统的一个重要组成部分，它对经济系统的运转和发展具有重要影响。经济系统则包含了更广泛的范围，它包括了生产、分配和消费等一系列经济活动和制度，而金融体系则是其中一个关键的子系统，用于为经济活动提供融资、风险管理、信息传递等服务。
    """
    def __init__(self,name):
        super().__init__(name)
    def provide_payment_system(self):
        # 提供支付系统，现金和电子支付
        pass

    def provide_funding(self):
        # 为借款人提供资金，即借贷
        pass

    def provide_market_liquidity(self):
        # 提供市场流动性，随时能够买卖金融资产
        pass

    def manage_risk(self):
        # 管理风险，包括金融机构和金融市场层面的风险管理
        pass

    def provide_information(self):
        # 提供信息，即价格和其他相关信息
        pass

    def provide_investment_opportunities(self):
        # 为投资者提供渠道，为他们提供投资选择和服务
        pass
