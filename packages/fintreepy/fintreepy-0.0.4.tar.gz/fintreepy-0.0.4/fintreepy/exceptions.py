class InitalValueNotInRangeError(Exception):
    """
    Exception raised for negative starting value. 
    """

    def __init__(self, message="Starting asset price must be non-negative"):
        super().__init__(message)


class TimeNotInRangeError(Exception):
    """
    Exception raised for negative time.
    """
    def __init__(self, message="Time must be non-negative"):
        super().__init__(message)


class BranchNotInRangeError(Exception):
    """
    Exception raised for insufficient number of branches. 
    """

    def __init__(self, message="Number of branches must be non-negative"):
        super().__init__(message)

class VolatilityNotInRangeError(Exception):
    """
    Exception raised for invalid volatility value
    """
    
    def __init__(self, message="Asset volatiltiy must be non-negative"):
        super().__init__(message)
