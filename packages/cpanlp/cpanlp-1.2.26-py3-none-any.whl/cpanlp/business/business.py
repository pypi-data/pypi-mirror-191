class Business:
    """
    ### ChatGPT:
    在商业世界中，operation指的是一个组织或企业所进行的具体业务活动和过程，如生产、采购、仓储、分销等。而business则是指企业的商业活动和经营行为，包括市场营销、战略规划、财务管理等，以实现盈利和成长。简而言之，operation是企业的具体操作活动，而business则是企业的总体管理和经营。
    """
    def __init__(self, name, industry):
        self.name = name
        self.industry = industry

    def description(self):
        return f"{self.name} is a business in the {self.industry} industry."
