class Relationship:
    def __init__(self, name1, name2, relationship_type):
        self.name1 = name1
        self.name2 = name2
        self.relationship_type = relationship_type

    def describe(self):
        return f"{self.name1} is {self.relationship_type} of {self.name2}"




