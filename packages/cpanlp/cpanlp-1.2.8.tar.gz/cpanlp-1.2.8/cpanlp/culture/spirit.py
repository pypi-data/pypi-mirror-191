class Spirit:
    def __init__(self,determination=0.0,passion=0.0,vision=0.0,risk_taking=0.0,innovation=0.0,perseverance=0.0,leadership=0.0,dedication=0.0,attention_to_detail=0.0):
        self.determination = determination
        self.passion = passion
        self.vision= vision
        self.risk_taking = risk_taking
        self.innovation = innovation
        self.perseverance = perseverance
        self.leadership =leadership
        self.dedication =dedication
        self.attention_to_detail = attention_to_detail
class Entrepreneurship(Spirit):
    def __init__(self,determination=6.0,passion=6.0,vision=6.0,risk_taking=6.0,innovation=6.0,perseverance=6.0,leadership=6.0,dedication=6.0,attention_to_detail=6.0):
        super().__init__(determination,passion,vision,risk_taking,innovation,perseverance,leadership,dedication,attention_to_detail)
        if not 6<=determination<=10:
            raise ValueError("determination must be between 6 and 10.")
        if not 6<=passion<=10:
            raise ValueError("passion must be between 6 and 10.")
        if not 6<=vision<=10:
            raise ValueError("vision must be between 6 and 10.")
        if not 6<=risk_taking<=10:
            raise ValueError("risk_taking must be between 6 and 10.")
        if not 6<=innovation<=10:
            raise ValueError("risk_taking must be between 6 and 10.")
        if not 6<=perseverance<=10:
            raise ValueError("risk_taking must be between 6 and 10.")
        if not 6<=leadership<=10:
            raise ValueError("risk_taking must be between 6 and 10.")
        if not 6<=dedication<=10:
            raise ValueError("risk_taking must be between 6 and 10.")
        if not 6<=attention_to_detail<=10:
            raise ValueError("risk_taking must be between 6 and 10.")
class Craftsmanship(Spirit):
    def __init__(self,determination=0.0,passion=0.0,vision=0.0,risk_taking=0.0,innovation=0.0,perseverance=0.0,leadership=0.0,dedication=6.0,attention_to_detail=6.0):
        super().__init__(determination,passion,vision,risk_taking,innovation,perseverance,leadership,dedication,attention_to_detail)
        if not 6<=dedication<=10:
            raise ValueError("risk_taking must be between 6 and 10.")
        if not 6<=attention_to_detail<=10:
            raise ValueError("risk_taking must be between 6 and 10.")
def main():
    a=Entrepreneurship()
    print(a.passion)
    b=Craftsmanship()
    print(b.dedication)
if __name__ == '__main__':
    main()