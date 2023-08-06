class GovernmentSubsidy:
    def __init__(self,name=None, product_or_service=None, original_price=None, subsidised_price=None,year=None, central_government_funds=None, special_funds=None):
        self.name = name
        self.product_or_service = product_or_service
        self.original_price = original_price
        self.subsidised_price = subsidised_price
        self.year = year
        self.central_government_funds = central_government_funds
        self.special_funds = special_funds
        
    def __str__(self):
        return "Government Subsidy: Year - {}, Central government funds - {} million, Special funds - {} million".format(
            self.year, self.central_government_funds, self.special_funds
        )
        
    def total_amount(self):
        return self.central_government_funds + self.special_funds
#GovernmentGrants" 和 "Subsidy" 都是政府的资金支持方式。但是，它们在某些方面存在差异：定义："Grants" 是指政府提供的不需要回报的资金，用于支持某些活动，而 "Subsidy" 是指政府对某些产品或服务的价格进行补贴，以使其价格更加实惠。用途：Grants 通常用于支持研究、开发、教育等项目，而 Subsidy 则用于减轻消费者或生产者的经济负担，并鼓励特定行业的生产和销售。条件：Grants 通常是在满足某些条件，如项目成果的公开或分享的情况下提供的，而 Subsidy 不需要满足任何特定的条件，只需要消费者购买或生产者生产该产品或服务。因此，"Grants" 和 "Subsidy" 都是政府的资金支持方式，但在定义、用途和条件方面存在差异。

def main():
    subsidy = GovernmentSubsidy(name="Renewable Energy", product_or_service="Solar Panels", original_price=10000, subsidised_price=8000)

if __name__ == '__main__':
    main()