class Operation:
    """
    ### ChatGPT:
    # 创建一个名为“生产”的操作对象
    production = Operation("生产", "将原材料转化为成品")

    # 执行该操作
    production.perform() 
    Performing operation '生产': 将原材料转化为成品
    可以创建其他操作对象，例如“采购”、“仓储”和“分销”，并调用它们的perform方法来模拟执行这些业务活动和过程。
    """
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def perform(self):
        print(f"Performing operation '{self.name}': {self.description}")
