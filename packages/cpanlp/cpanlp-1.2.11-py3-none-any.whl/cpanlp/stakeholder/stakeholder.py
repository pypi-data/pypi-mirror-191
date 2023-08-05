from cpanlp.entity.entity import *

class Stakeholder(LegalEntity):
    def __init__(self, name,type=None,capital=None, interests=None,power=None):
        super().__init__(name,type,capital)
        self.name = name
        self.interests = interests
        self.power = power
        self.contact_info = ""
        self.concern=""
        self.suggest=""

def main():
    print("hello")
if __name__ == '__main__':
    main()