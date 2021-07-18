
from Derivatives.Derivative import Derivative

class Option(Derivative):
    
    def __init__(self, S0, K, T, r, s, option_type, position_type, contract_size, multiplier):
        Derivative.__init__(self, S0, K, T, r, position_type, contract_size, multiplier)
        self.s = s
        self.option_type = option_type
        self.price = 0
        self.delta = 0
        self.gamma = 0
        self.vega = 0
    
    def get_option_properties(self):
        option_1 = self
        print('Properties of the call @ Strike: ', option_1.K)
        print('-----------------------------------')
        for i in vars(option_1):
            print(i, ':', vars(option_1)[i])
            
    def get_option_payoff(self):
        pass
         
            
            
