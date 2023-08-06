from cpanlp.person.consumer import *

class Founder(Consumer):
    def __init__(self,name=None, age=None,wealth=None,utility_function=None, subscribed_shares=None, subscribed_shares_unit=None, ownership_ratio=None, funding_method=None):
        super().__init__(name, age,wealth,utility_function)
        self.subscribed_shares = subscribed_shares
        self.subscribed_shares_unit = subscribed_shares_unit
        self.ownership_ratio = ownership_ratio
        self.funding_method = funding_method

    def set_subscribed_shares(self, subscribed_shares):
        self.subscribed_shares = subscribed_shares

    def set_subscribed_shares_unit(self, subscribed_shares_unit):
        self.subscribed_shares_unit = subscribed_shares_unit

    def set_ownership_ratio(self, ownership_ratio):
        self.ownership_ratio = ownership_ratio

    def set_funding_method(self, funding_method):
        self.funding_method = funding_method
#"Founder" 通常是指创建公司的人，他们是公司的核心人物，负责制定公司的愿景、目标和战略，并为公司的发展奠定基础。

#"Entrepreneur" 则是更广泛的概念，指的是那些敢于创业、承担商业风险、追求经济回报的人。他们可以是创办公司的人，也可以是独立创业者，或是在已有公司内部进行创业。

#因此，可以说 "Founder" 和 "Entrepreneur" 是相关的，但是 "Founder" 专门指的是创建公司的人，而 "Entrepreneur" 指的是更广泛的创业者范畴。


