#高管离职适合单独写一个类。离职是一个独立的事件，不属于高管的常规行为，因此它应该是一个单独的类。这样可以更好地隔离它，更方便维护代码和扩展功能。
#Severance package 是一种离职补偿的形式，通常是在员工被解雇或者辞去工作的情况下由公司提供的。这种补偿通常包括现金以及一些其他的福利，例如：赔偿金：为员工在离职之后的生活和就业做好准备的现金补贴。保险：例如医疗保险，补充医疗保险等。出险补助：为员工处理离职所带来的后遗症提供的资金。工作培训：为员工找到新工作提供的职业培训和职业发展机会。Severance package 的数额和内容因公司的不同而不同，也可能因员工的职位、工作年限、工作表现等因素有所不同。
class Resignation:
    def __init__(self, name, reason=None, notice_period=None, final_day=None, severance_package=None):
        self.name = name
        self.reason = reason
        self.notice_period = notice_period
        self.final_day = final_day
        self.severance_package = severance_package
    def resign(self):
        print(f"{self.name} has resigned due to {self.reason} with a notice period of {self.notice_period}.")






