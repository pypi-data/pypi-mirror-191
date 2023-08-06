from pricetree import PriceTree
import math

class TrinomialPriceTree(PriceTree):
    def gen_parameters(self):
        # Moddeling values
        self.dt = self.t / self.b
        #Up/Down Factor
        # https://warwick.ac.uk/fac/sci/maths/people/staff/oleg_zaboronski/fm/trinomial_tree_2009.pdf
        self.u = math.e ** (self.v * ((2 * self.dt) ** 0.5))
        self.d = 1 / self.u
        # Probabilities
        denominator = math.e ** (self.v * (self.dt / 2) ** 0.5) - math.e ** (-self.v * (self.dt / 2) ** 0.5)
        self.p = ((math.e ** (self.r * self.dt / 2 ) - math.e ** (-self.v * (self.dt / 2) ** 0.5)) / denominator) ** 2
        self.q = ((-math.e ** (self.r * self.dt / 2 ) + math.e ** (-self.v * (self.dt / 2) ** 0.5)) / denominator) ** 2
        self.m = 1 - self.p - self.q
    
    def gen_tree(self):
        self.Tree = [[self.s]]
        for row in range(self.b):
            self.Tree.append([self.Tree[-1][0] * self.d] + self.Tree[-1] + [self.Tree[-1][-1] * self.u])
    
    def value_options(self):
        pass