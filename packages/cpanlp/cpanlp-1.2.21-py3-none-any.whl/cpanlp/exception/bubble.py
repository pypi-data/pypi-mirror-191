
        
class StockMarketBubble(Exception):
    def __init__(self,message="Stock market bubble detected!"):
        self.message = message
        super().__init__(self.message)
def main():
    if 11 > 10:
    # Code that may cause a stock market bubble exception
        raise StockMarketBubble()
if __name__ == '__main__':
    main()