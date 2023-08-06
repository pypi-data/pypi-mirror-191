class Activity:
    """
    ### ChatGPT:

    在商业世界中，Activity和Operation是两个相关但不同的概念。

    Activity指的是一系列的活动或过程，通常与某个目标或结果相关联。例如，市场营销活动、生产活动或财务活动等。Activity通常涉及多个步骤和参与
    者，并且可能需要跨越多个部门或团队。

    Operation指的是一个特定的商业活动或过程，通常是指一个特定的业务功能或部门。例如，生产操作、销售操作或客户服务操作等。Operation通常是一个
    组织的核心业务，需要专门的资源和专业知识来管理和执行。

    因此，Activity和Operation之间的区别在于，Activity更加广泛，通常涉及多个部门或团队，而Operation则更加专业化，通常涉及特定的业务功能或
    部门。但是，Activity和Operation之间也存在联系，因为Activity通常由一系列的Operation组成，而Operation则可以作为Activity的一部分。
    """
    def __init__(self, name, value_added):
        self.name = name
        self.value_added = value_added

    def get_name(self):
        return self.name

    def get_value_added(self):
        return self.value_added
