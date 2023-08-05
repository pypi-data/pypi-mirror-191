class PonziScheme:
    def __init__(self, promise):
        self.promise = promise
        self.victims = []
    def add_victim(self, victim):
        self.victims.append(victim)
    def get_info(self):
        print(f"Promise: {self.promise}")
        print(f"Number of victims: {len(self.victims)}")