
    
class WinnerCurse(Exception):
    def __init__(self,message="You are cursed to lose after winning!"):
        self.message = message
        super().__init__(self.message)
def main():
    if 11 > 10:
    # Code that may cause a stock market bubble exception
        raise WinnerCurse()
if __name__ == '__main__':
    main()