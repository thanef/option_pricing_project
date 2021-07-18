class Derivative:
    
    def __init__(self, S0, K, T, r, position_type, contract_size, multiplier):
        self.S0 = S0
        self.K = K
        self.T = T
        self.r = r
        self.position_type = position_type
        self.contract_size = contract_size
        self.multiplier = multiplier
        self.payoff = 0