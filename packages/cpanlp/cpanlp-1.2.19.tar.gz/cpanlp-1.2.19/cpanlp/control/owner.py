#Beneficial owner 指的是拥有或控制资产或财产的人，尽管它可能是通过代理人或其他形式控制的。这意味着，即使资产或财产在法律上归某人所有，但如果另一人控制了这些资产或财产，则该人可被视为有益所有人。

#例如，如果一个人将股票存入信托基金，信托基金将是法律上的所有者，但该人仍将是有益所有人，因为他控制了该股票。

#在金融和法律领域中，确定有益所有人的信息非常重要，因为它可以帮助监管机构了解资金的来源和流向，以及识别潜在的非法活动。
class Owner:
    def __init__(self, name, ownership_percentage, assets):
        self.name = name
        self.assets = assets
        self.ownership_percentage = ownership_percentage
    def __str__(self):
        return f"Name: {self.name}\nAssets: {self.assets}"

class BeneficialOwner(Owner):
    def __init__(self, name, assets,control_via,ownership_percentage=None):
        super().__init__(name, ownership_percentage, assets)
        self.control_via = control_via

    def __str__(self):
        return f"Name: {self.name}\nOwnership Percentage: {self.ownership_percentage}%\nAssets: {self.assets}"
