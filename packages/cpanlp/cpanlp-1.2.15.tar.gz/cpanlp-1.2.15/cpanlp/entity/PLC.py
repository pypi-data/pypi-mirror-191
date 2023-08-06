from cpanlp.entity.LLC import *
class PLC(LLC):
    def __init__(self,name,type=None,capital=None):
        super().__init__(name,type,capital)
        self.shareholders=[]
def main():
    print("hello")
    a=PLC("华为","niu",1000)
if __name__ == '__main__':
    main()