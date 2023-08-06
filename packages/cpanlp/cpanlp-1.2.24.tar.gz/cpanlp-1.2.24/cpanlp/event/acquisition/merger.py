#Acquisition 和 Merger 是指企业的并购的两个术语。

#Acquisition 指的是一家公司收购另一家公司，并成为收购公司的一部分。收购公司通常通过股权收购或其他形式的资本投入获得对目标公司的控制。

#Merger 指的是两家公司合并为一家新公司，并通常具有新的股权结构和管理团队。在合并中，原先的两家公司不再存在，投资者只能持有新公司的股份。

#因此，Acquisition 和 Merger 的关系是合并的一种形式，Acquisition 更多的是收购，Merger 更多的是合并。在某些情况下，Acquisition 可以成为合并的前奏，并在进一步的合并过程中实现。
class Merger:
    def __init__(self, target_company, acquiring_company, merger_price=None,date=None):
        self.target_company = target_company
        self.acquiring_company = acquiring_company
        self.merger_price = merger_price
        self.date =date
