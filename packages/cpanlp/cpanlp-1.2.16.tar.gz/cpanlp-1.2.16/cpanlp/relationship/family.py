from cpanlp.relationship.relationship import *

class Family(Relationship):
    def __init__(self, name1, name2, relationship_type):
        super().__init__(name1, name2, relationship_type)

father = Family("John", "Jane", "father")