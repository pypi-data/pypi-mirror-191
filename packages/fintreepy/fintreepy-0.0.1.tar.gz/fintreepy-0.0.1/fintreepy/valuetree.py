class ValueTree:
    """
    Stores the pricing data for an option.
    
    Parameters
    ----------
    tree : List of Nodes
        The values of the tree at each step of the tree stored in a Node.
        
    """
    
    def __init__(self, tree):
        self._tree = tree
        self.price = tree[0][0].price
        
    def save_vars(self, i, conv_ratio, fv, u, d, p, m, q):
        self.i = i
        self.conv_ratio = conv_ratio
        # self.c = c
        self.fv = fv
        self.u = u
        self.d = d
        self.p = p
        self.m = m
        self.q = q
    
    def get_vars(self):
        return [self.i, self.conv_ratio, self.c, self.fv, self.u, self.d, self.p, self.m, self.q]
        
    def get_tree(self):
        return self._tree
    
    def get_head(self):
        return self._tree[0][0]
    
    def get_price(self):
        """
        Returns the fair value of the option.

        Returns
        -------
        Float
            The fair value of the option.

        """
        return self.price
    
    def get_prices(self):
        """
        Returns the value of the asset at each branch in the tree.
        
        Each list represents another branch

        Returns
        -------
        List
            Price of the asset at each node

        """
        vals = []
        for branch in self._tree:
            b = []
            for node in branch:
                b.append(node.price)
            vals.append(b)
        return(vals)