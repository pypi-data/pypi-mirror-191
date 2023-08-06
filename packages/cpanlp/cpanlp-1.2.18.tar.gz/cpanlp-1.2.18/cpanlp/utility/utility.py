import math
import numpy as np
import matplotlib.pyplot as plt
class CRRA:
    def __init__(self, gamma):
        self.gamma = gamma
    def utility(self, c):
        if self.gamma == 1.:
            return np.log(c)
        else:
            return (c ** (1 - self.gamma)) / (1 - self.gamma)
class CRRAInvestor(CRRA):
    def __init__(self, gamma, rho):
        super().__init__(gamma)
        self.rho = rho
    def utility(self, c, w):
        if self.gamma == 1:
            return np.log(c) + self.rho * np.log(w)
        else:
            return (c ** (1 - self.gamma)) / (1 - self.gamma) + self.rho * (w ** (1 - self.gamma)) / (1 - self.gamma)
def main():
    c=CRRA(0.2)
    print(c.utility(100))
    d=CRRAInvestor(0.4,0.2)
    print(d.utility(100,3000))
if __name__ == '__main__':
    main()