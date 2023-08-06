class Capacity:
    def __init__(self, maximum_capacity, current_capacity):
        self.maximum_capacity = maximum_capacity
        self.current_capacity = current_capacity
    @property
    def is_saturated(self):
        return self.current_capacity >= self.maximum_capacity