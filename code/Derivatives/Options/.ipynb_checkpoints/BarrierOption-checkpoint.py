from Derivatives.Options.Option import Option
from math import *
from numpy import *
import scipy.stats as si

class BarrierOption(Option):
    
    def __init__(self, S0, K, T, r, s, option_type, position_type, contract_size, multiplier, barrier_type, barrier, q):
        Option.__init__(self, S0, K, T, r, s, option_type, position_type, contract_size, multiplier)
        self.barrier_type = barrier_type
        self.barrier = barrier
        self.q = q
        
    # Get option price using closed-end formula of Black & Scholes
    def calculate_option_price_BS_formula(self):
        
        S0, K, r, T, s, option_type = self.S0, self.K, self.r, self.T, self.s, self.option_type
        barrier, barrier_type, q = self.barrier, self.barrier_type, self.q
        
        # Paramaters d1, d2, lamda and y of the Black & Scholes closed end formula for pricing Barrier options
        d1 = (log(S0/K) + (r + (s**2/2))*T)/(s*sqrt(T))
        d2 = d1 - (s*sqrt(T))
                
        lamda = (r - q + (s ** 2 /2)) / (s ** 2)                   
        y = log((barrier ** 2) / (S0 * K))/(s * sqrt(T))     
         
        # in addition, parameters x1 and y1 for H >= K
        x1 = ((log(S0/barrier))/(s*sqrt(T))) + (lamda*s*sqrt(T))
        y1 = ((log(barrier/S0))/(s*sqrt(T))) + (lamda*s*sqrt(T))

        if option_type == 'call':
            option_price = S0*si.norm.cdf(d1, 0.0, 1.0) - K*exp(-r * T)*si.norm.cdf(d2, 0.0, 1.0)
            if barrier_type == 'down-and-in':
                if barrier < K:
                    option_price = S0 * exp(-q * T)*((((barrier/S0) ** (2*lamda)) * si.norm.cdf(y, 0.0, 1.0))) - K * exp(-r*T)*( (((barrier/S0) ** (2*lamda - 2)) *  si.norm.cdf(y - (s*sqrt(T)), 0.0, 1.0)))
                else:
                    option_price = S0 * exp(-q * T) * (si.norm.cdf(d1, 0.0, 1.0) - si.norm.cdf(x1, 0.0, 1.0) + (((barrier/S0)**(2*lamda))*si.norm.cdf(y1, 0.0, 1.0))) - K * exp(-r*T) * (si.norm.cdf(d2, 0.0, 1.0) - si.norm.cdf(x1 - (s*sqrt(T)), 0.0, 1.0) + (((barrier/S0)**(2*lamda - 2))*si.norm.cdf(y1 - (s*sqrt(T)), 0.0, 1.0)))
            elif barrier_type == 'down-and-out':
                if barrier < K:
                    option_price = S0 * exp(-q * T)*(si.norm.cdf(d1, 0.0, 1.0) - (((barrier/S0) ** (2*lamda)) * si.norm.cdf(y, 0.0, 1.0))) + K * exp(-r*T)*( (((barrier/S0) ** (2*lamda - 2)) *  si.norm.cdf(y - (s*sqrt(T)), 0.0, 1.0)) - si.norm.cdf(d2, 0.0, 1.0))
                else:
                    option_price = S0 * exp(-q * T) * (si.norm.cdf(x1, 0.0, 1.0) - (((barrier/S0)**(2*lamda))*si.norm.cdf(y1, 0.0, 1.0))) - K * exp(-r*T) * (si.norm.cdf(x1 - (s*sqrt(T)), 0.0, 1.0) - (((barrier/S0)**(2*lamda - 2))*si.norm.cdf(y1 - (s*sqrt(T)), 0.0, 1.0)))
            else:
                pass
                
        elif option_type == 'put':
            pass
        else:
            print("Give a proper option type")
        
        self.price = option_price
        self.payoff = self.get_option_payoff()
        
        return option_price
    
    
    
    def get_option_payoff(self):
        super().get_option_payoff()
        
        S0, K, r, T, s, option_type = self.S0, self.K, self.r, self.T, self.s, self.option_type
        position_type, contract_size, multiplier = self.position_type, self.contract_size, self.multiplier
        barrier, barrier_type, q = self.barrier, self.barrier_type, self.q
            
        ceiling = math.ceil(2 * S0) # assuming that the underlying is the same for all the options, we put a limit of the spot price as 2x the current price
        spot_price_table = linspace(0, ceiling, ceiling*10, endpoint=False)  #create the table of spot prices so as to compute the payoff
        payoff = [0]*len(spot_price_table)
        for i in range(0,len(spot_price_table),1):
            if position_type == 'Long':
                if barrier_type == 'down-and-in':
                    if barrier <= spot_price_table[i]:
                        payoff[i] = (maximum(spot_price_table[i]-K, 0) * contract_size * multiplier) + payoff[i]
                    else:
                        payoff[i] = 0
                elif barrier_type == 'down-and-out':
                    if barrier <= spot_price_table[i]:
                        payoff[i] = 0
                    else:
                        payoff[i] = (maximum(spot_price_table[i]-K, 0) * contract_size * multiplier) + payoff[i]
                else:
                    pass
            elif position_type == 'Short':
                if barrier_type == 'down-and-in':
                    if barrier <= spot_price_table[i]:
                        payoff[i] = payoff[i] = (-maximum(spot_price_table[i]-K,0) * contract_size * multiplier) + payoff[i]
                    else:
                        payoff[i] = 0
                elif barrier_type == 'down-and-out':
                    if barrier <= spot_price_table[i]:
                        payoff[i] = 0
                    else:
                        payoff[i] = (-maximum(spot_price_table[i]-K,0) * contract_size * multiplier) + payoff[i]
                else:
                    pass
            else: 
                print("Please give either Long or Short for the position type")
            payoff[i] = round(payoff[i],2)
        
        return payoff
    
    