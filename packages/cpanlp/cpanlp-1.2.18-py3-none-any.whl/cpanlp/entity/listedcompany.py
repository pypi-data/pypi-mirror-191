from cpanlp.entity.PLC import *
class ListedCompany(PLC):
    def __init__(self,name,type=None,capital=None):
        super().__init__(name,type,capital)
        self.shareholders=[]
def main():
    print("hello")
    a=ListedCompany("华为","niu",1000)

if __name__ == '__main__':
    main()