import math
from fintreepy.node import Node
from fintreepy.valuetree import ValueTree
from fintreepy.exceptions import InitalValueNotInRangeError, TimeNotInRangeError, BranchNotInRangeError, VolatilityNotInRangeError

class PriceTree:
    """
    Create a binomial price tree for an asset.

    Parameters
    ----------
    s : Float
        Starting price of the asset.
    t : Float
        Number of years to create tree for.
    r : Float
        Annual risk-free rate.
    b : Int
        Number of branches in the tree.
    v : Float
        Volatility of the Underlying Asset

    """
    def __init__(self, s, t, r, b, v):
        self.validate_inputs(s, t, r, b, v)

        self.s = s
        self.t = t
        self.r = r
        self.b = b
        self.v = v
        
        self.vars = {'s': self.s, 't': self.t, 'r': self.r, 'b': self.b, 'v': self.v}
        
        self.gen_parameters()
        self.gen_tree()

    def validate_inputs(self, s, t, r, b, v):
        if s < 0:
            raise InitalValueNotInRangeError()

        if t < 0:
            raise TimeNotInRangeError()

        if b < 0:
            raise BranchNotInRangeError()

        if v < 0:
            raise VolatilityNotInRangeError()
        
    def get_vars(self):
        """
        Returns the variables used to create the PriceTree.

        Returns
        -------
        list
            Returns the current values of spot rate, time, risk-free rate,
            branches, volatility and time per branch.

        """
        return [self.s, self.t, self.r, self.b, self.v, self.dt]
        
    def change_vars(self, **kwargs):
        # TODO - MAKE VARIABLE CHANGER WORK
        for variable in kwargs:
            if variable in self.vars.keys():
                self.vars[variable] = kwargs[variable]
                
        self.gen_parameters()
        self.gen_tree()

    def gen_parameters(self):
        """
        Calulcates parameters for current variables to build the tree.
        
        These prameters are the time per branch, the up and down factors and
        the probability of up and down movements.

        """
        # Moddeling values
        self.dt = self.t / self.b
        #Up/Down Factor
        self.u = math.e ** (self.v * (self.dt ** 0.5))
        self.d = 1/self.u
        # Probabilities
        self.p = (math.e ** (self.r * (self.dt)) - self.d) / (self.u - self.d)
        self.q = (1-self.p)
    
    def gen_tree(self):
        """
        Use the current variables to gemerate the price tree of the underlying
        asset.

        """
        
        # TODO: Trial if copying two branches ago and adding one each side is faster
        if not self.b:
            self.Tree = [[self.s]]

        else:
            self.Tree = [[self.s], [self.s * self.d, self.s * self.u]]
            for row in range(1, self.b): 
                self.Tree.append([self.Tree[-1][0] * self.d] + self.Tree[-2] + [self.Tree[-1][-1] * self.u])

            # self.Tree = [[self.s], [self.s * self.d, self.s * self.u]]
            # for row in range(1, self.b):
            #     newRow = [self.Tree[row][0] * self.d]
            #     for item in self.Tree[row]:
            #         newRow.append(item * self.u) 
            #     self.Tree.append(newRow)
            
    def value_option(self, x, nat = 'A', typ = 'C', func = None, prnt = False):
        """
        Value an option on the underlying asset.
        
        Assumes non-negative asset values at every branch

        Parameters
        ----------
        x : Float
            The exercise price of the option
        nat : String, optional
            The nationality of the option, 'A' for American, 'E' for European. 
            The default is 'A'.
        typ : String, optional
            The type of option to value, 'C' for Call, 'P' for Put, 'E' for
            Exotic. The default is 'C'.
        func : function, optional
            If valuing an exotic option provide a function that will determine 
            the intrinsic value of the option. Must take the stock price at the 
            current branch as the first parameter and the exercise price as the 
            second.
        prnt : bool, optional
            If the price will be printed to console. The default is True.
            
        Returns
        -------
        ValueTree
            ValueTree object that contains the fair value of the option and the
            value at each node.

        """
        # Default functions for calls/puts
        call = lambda p, e: max(p - e, 0)
        put = lambda p, e: max(e - p, 0)
        
        # Choose desired IV function
        if typ == 'C':
            func = call
        if typ == 'P':
            func = put
        if typ == 'E':
            func = func
        
        valuetree = []
        new_row = []
        # Value last branch as there is no DCF method, only IV
        for item in self.Tree[-1]:
            new_row.append(Node(0, func(item, x)))
        valuetree.append(new_row)
        
        # Value remaining branches backwards, as require last node's value
        for branch in self.Tree[:-1][::-1]:
            new_row = []
            for item in range(len(branch)):
                # Value using DCF method,as branch always one smaller than the last,
                # gets same index from last branch for lower value and upper branch for
                # the higher value
                lower = valuetree[-1][item].price
                upper = valuetree[-1][item+1].price
                dcf = math.e ** (-self.r * self.dt) * (self.p * upper + self.q * lower)
                
                # Second term passes the IV if nat is A, otherwise will be 0 and 
                # DCF value will be used as prices are always greater than 0.
                new_row.append(Node(dcf, [0, func(branch[item], x)][nat=='A']))
            valuetree.append(new_row)
            
        valuetree = valuetree[::-1]
        
        if prnt:
            print(valuetree[0][0].price)
            
        return ValueTree(valuetree)

    def get_prices(self):
        """
        Returns the value of the asset at each branch in the tree.
        
        Each list represents another branch

        Returns
        -------
        List
            Price of the asset at each node

        """
        return self.Tree
    

class OldPriceTree(PriceTree):
    def gen_tree(self):
        """
        Use the current variables to gemerate the price tree of the underlying
        asset.

        """
        
        # TODO: Trial if copying two branches ago and adding one each side is faster
        if not self.b:
            self.Tree = [[self.s]]

        else:
            self.Tree = [[self.s], [self.s * self.d, self.s * self.u]]
            for row in range(1, self.b):
                newRow = [self.Tree[row][0] * self.d]
                for item in self.Tree[row]:
                    newRow.append(item * self.u) 
                self.Tree.append(newRow)