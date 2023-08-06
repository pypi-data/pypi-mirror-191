class Node:
    """
    Stores the price data for each point in the ValueTree object.
    
    Takes the discoutned value and intrinsic value at a branch and determines the value.
    
    Parameters
    ----------
    dcf : Float
        The value at the node using the discounted cash flow method.
    iv : Float, optional
        The intrinsice value of the option at the node.
    
    """
    def __init__(self, dcf, iv=0):
        self.dcf = dcf
        self.iv = iv
        self.price = max(dcf, iv)