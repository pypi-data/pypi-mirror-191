
class AbnormalFluctuation(Exception):
    def __init__(self, stock_name, percent_change):
        self.stock_name = stock_name
        self.percent_change = percent_change
        self.message = f"Stock {self.stock_name} had an abnormal change of {self.percent_change}%"
        super().__init__(self.message)
def main():
    def trade_stock(stock_name, current_price, previous_price):
        percent_change = (current_price - previous_price) / previous_price * 100
        if abs(percent_change) > 10:
            raise AbnormalFluctuation(stock_name, percent_change)
    trade_stock("dd",19,111)
if __name__ == '__main__':
    main()