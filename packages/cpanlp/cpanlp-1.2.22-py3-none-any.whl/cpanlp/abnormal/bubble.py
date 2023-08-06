from datetime import datetime
from typing import Optional
class Bubble:
    """
    #### This class represents an asset bubble.
    
    Attributes:
    asset (int): asset_name
    bubble_start_date (str):  start date of the bubble, '%Y-%m-%d'
    bubble_end_date (str): end date of the bubble, '%Y-%m-%d'
    peak_value (float): the peak value of the asset during the bubble
    burst_value (float):the value of the asset after the bubble has burst
    
    #### This class calculates and initializes the following instance variables based on the input arguments.
    
    duration (int): number of days between the start and end dates of the bubble
    peak_to_burst_difference (float): difference between the peak value and burst value of the asset
    is_burst (bool): whether the bubble has burst or not, initially set to False
    
    Example:
    ```
    bitcoin_bubble = Bubble("bitcoin","2010-01-01","2025-01-01",100000,50000)
    print(bitcoin_bubble.is_burst) # False
    ```
    Learn more about Bubble in the [official documentation](https://cpanlp.com).
    """
    def __init__(self, asset, bubble_start_date: str, bubble_end_date: str, peak_value: float, burst_value: float):
        self.asset = asset
        self.bubble_start_date = datetime.strptime(bubble_start_date, '%Y-%m-%d')
        self.bubble_end_date = datetime.strptime(bubble_end_date, '%Y-%m-%d')
        self.peak_value = peak_value
        self.burst_value = burst_value
        self.duration= (self.bubble_end_date - self.bubble_start_date).days
        self.peak_to_burst_difference = self.peak_value - self.burst_value
        self.is_burst = False
    def sum(self):
        print(f'Asset: {self.asset}')
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