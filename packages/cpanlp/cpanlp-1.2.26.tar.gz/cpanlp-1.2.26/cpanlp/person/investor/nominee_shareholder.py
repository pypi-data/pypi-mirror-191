#Nominee Shareholder 是一种指定代表人，代表实际持股人持有股票的实体。在这种情况下，实际持股人委托 Nominee Shareholder 代表他们持有股票，并执行相关股权交易。

#Nominee Shareholder 一般用于保护实际持股人的隐私，或者避免实际持股人需要暴露自己的身份。然而，使用 Nominee Shareholder 也可能导致治理问题，因为实际持股人可能不能直接参与公司决策。因此，在使用 Nominee Shareholder 时应该仔细考虑相关法律法规和风险。
from cpanlp.person.investor.shareholder import *

class NomineeShareholder(Shareholder):
    def __init__(self,actual_shareholder, name, age, wealth,utility_function,portfolio, expected_return, risk_preference,shares):
        super().__init__(name, age, wealth,utility_function,portfolio, expected_return, risk_preference,shares)
        self.actual_shareholder = actual_shareholder