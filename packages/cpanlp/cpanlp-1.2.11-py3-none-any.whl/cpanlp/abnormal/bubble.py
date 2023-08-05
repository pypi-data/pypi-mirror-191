from datetime import datetime

class Bubble:
    def __init__(self, asset_name, bubble_start_date, bubble_end_date, peak_value, burst_value):
        self.asset_name = asset_name
        self.bubble_start_date = datetime.strptime(bubble_start_date, '%Y-%m-%d')
        self.bubble_end_date = datetime.strptime(bubble_end_date, '%Y-%m-%d')
        self.peak_value = peak_value
        self.burst_value = burst_value
        self.duration= (self.bubble_end_date - self.bubble_start_date).days
        self.peak_to_burst_difference = self.peak_value - self.burst_value
        self.is_burst = False
    def sum(self):
        print(f'Asset: {self.asset_name}')
        print(f'Duration: {self.duration}')
        print(f'Peak Value: {self.peak_value}')
        print(f'Burst Value: {self.burst_value}')
        print(f'Peak to Burst Difference: {self.peak_to_burst_difference}')
def main():
    bu=Bubble("gold","2014-01-01","2024-01-01",10000,1000)
    print(bu.duration)
    print(bu.peak_to_burst_difference)
    bu.sum()
if __name__ == '__main__':
    main()