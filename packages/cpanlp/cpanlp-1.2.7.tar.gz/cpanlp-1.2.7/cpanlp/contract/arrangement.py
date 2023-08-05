#"Agreement" 和 "Arrangement" 都是英语中常见的协议术语，用于描述两方或多方之间的协商和达成的协议。但是，在某些情况下，两者有一些明显的差别：

#"Agreement" 通常指的是一项正式的、书面的、有法律效力的协议，如合同、协议等。

#"Arrangement" 通常指的是一项非正式的、口头的、没有法律效力的协议，如安排、协商等。
class Arrangement:
    def __init__(self, parties=None, purpose=None, terms=None):
        self.parties = parties
        self.purpose = purpose
        self.terms = terms
        self.enforceability = False