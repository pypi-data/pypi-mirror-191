from cpanlp.culture.spirit.spirit import *

class Craftsmanship(Spirit):
    def __init__(self,determination=0.0,passion=0.0,vision=0.0,risk_taking=0.0,innovation=0.0,perseverance=0.0,leadership=0.0,dedication=6.0,attention_to_detail=6.0):
        super().__init__(determination,passion,vision,risk_taking,innovation,perseverance,leadership,dedication,attention_to_detail)
        if not 6<=dedication<=10:
            raise ValueError("risk_taking must be between 6 and 10.")
        if not 6<=attention_to_detail<=10:
            raise ValueError("risk_taking must be between 6 and 10.")
def main():
    b=Craftsmanship()
    print(b.dedication)
if __name__ == '__main__':
    main()