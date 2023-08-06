from cpanlp.information.signal import *
keyword = "你好"
#例如，在劳动市场中，一个人的学历可以被看作是对他的工作能力的一种信号，而他的工作能力则是信息。信号和信息之间的关系是相互依存的。信号需要信息来提供意义，而信息需要信号来传递。信号传递信息是有成本的，所以在经济学中信号传递的成本称为信息成本。        
class Information:
    def __init__(self, message):
        self.message=message
        self.signals = []
        self.value=0.0
    @property
    def signal(self): 
        words = self.message.split()
        for i in range(len(words)):
            if keyword in words[i]:
                self.signals.append(" ".join(words[i:i+3]))
        return self.signals
    @property
    def send_signal(self):
        return Signal(self.signals)
class PositiveInformation(Information):
    def __init__(self, message,credibility, impact):
        super().__init__(message)
        self.credibility = credibility
        self.impact = impact
