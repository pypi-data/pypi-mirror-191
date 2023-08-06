from cpanlp.person.consumer import *
#"Reporting person"是指在美国证券市场监管机构（如美国证券交易委员会）的披露文件（如Insider Trading Reports）中报告关于内部人员的股票买卖行为的个人或公司。
class ReportingPerson(Consumer):
    def __init__(self, name,company=None, title=None, transaction_date=None,share=None, age=None,wealth=None,utility_function=None):
        super().__init__(name, age,wealth,utility_function)
        self.share = share
        self.company = company
        self.title=title
        self.transaction_date =transaction_date