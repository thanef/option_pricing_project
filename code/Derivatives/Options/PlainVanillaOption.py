from math import *
from numpy import *
import scipy.stats as si
from matplotlib import pyplot
from Derivatives.Options.Option import Option

class PlainVanillaOption(Option):
    
    def __init__(self, S0, K, T, r, s, option_type, position_type, contract_size, multiplier):
        Option.__init__(self, S0, K, T, r, s, option_type, position_type, contract_size, multiplier)
        
    # Get option price using closed-end formula of Black & Scholes
    def calculate_option_price_BS_formula(self):
        
        S0, K, r, T, s, option_type = self.S0, self.K, self.r, self.T, self.s, self.option_type
        
        d1 = (log(S0/K) + (r + (s**2/2))*T)/(s*math.sqrt(T))
        d2 = d1 - (s*math.sqrt(T))
        
        if option_type == 'call':
            option_price = S0*si.norm.cdf(d1, 0.0, 1.0) - K*exp(-r * T)*si.norm.cdf(d2, 0.0, 1.0)
        elif option_type == 'put':
            option_price = K*exp(-r * T)*si.norm.cdf(-d2, 0.0, 1.0) - S0*si.norm.cdf(-d1, 0.0, 1.0)
        else:
            print("Give a proper option type")
        
        self.price = option_price
        self.payoff = self.get_option_payoff()
        
        return option_price
    
    
    # Get option price using Monte carlo simulation
    def calculate_option_price_MC_BS(self):
        
        # Parameters
        S0, K, r, T, s, option_type = self.S0, self.K, self.r, self.T, self.s, self.option_type
       
        M = 50; dt = T / M; I = 10000
        # Simulating I paths with M time steps
        
        S = S0 * exp(cumsum((r - 0.5 * s ** 2) * dt
+ s * math.sqrt(dt)
* random.standard_normal((M + 1, I)), axis=0))
        
        # sum instead of cumsum would also do
        # if only the final values are of interest
        S[0] = S0
        # Calculating the Monte Carlo estimator
        
        if option_type == 'call':
            option_price_MC = math.exp(-r * T) * sum(maximum(S[-1] - K, 0)) / I
        elif option_type == 'put':
            option_price_MC = math.exp(-r * T) * sum(maximum(K - S[-1], 0)) / I
        else:
            print("Give a proper option type")
            
        #print('The European', option_type, 'option Value is: ', option_price_MC)
        
        self.get_graphical_visualization(S) # Uncomment for some plotting
        
        self.price = option_price_MC
        self.payoff = self.get_option_payoff()
        
    #Calculate option Greeks
    def calculate_option_greeks(self):
        
        S0, K, r, T, s, option_type = self.S0, self.K, self.r, self.T, self.s, self.option_type
        
        d1 = (log(S0/K) + (r + (s**2/2))*T)/(s*math.sqrt(T))
        
        if option_type == 'call':
            delta = si.norm.cdf(d1, 0.0, 1.0) #Delta of the call option
        elif option_type == 'put':
            delta = -si.norm.cdf(-d1, 0.0, 1.0) #Delta of the put option
        else:
            print("Give a proper option type")
            
        
        gamma = si.norm.pdf(d1,0.0, 1.0)/(S0*s*math.sqrt(T))  #Gamma of the call or put option
        vega = si.norm.pdf(d1,0.0, 1.0)*S0*math.sqrt(T)
        
        self.delta = delta
        self.gamma = gamma
        self.vega = vega
        
        greeks = {'delta':delta, 'gamma':gamma, 'vega': vega }
        
        #return greeks
    
    def get_graphical_visualization(self, S):
        
        strike_price = self.K
        
        # Graphical visualization of simulated paths
        pyplot.title('Monte Carlo simulation scenarios')
        pyplot.plot(S[:, :100])
        pyplot.grid(True)
        pyplot.xlabel('Steps')
        pyplot.ylabel('Underlying Price level')
        pyplot.show()
        
        # Histogram of Underlying market value at time T
        pyplot.title('Histogram: simulated end-of-period spot prices')
        #pyplot.rcParams["figure.figsize"] = (10,3)
        pyplot.hist(S[-1], bins=50)
        pyplot.grid(True)
        pyplot.xlabel('Underlying Price level')
        pyplot.ylabel('frequency')
        pyplot.show()
        
        # Payoff of the Option at time T
        pyplot.title('Histogram: simulated option values')
        #pyplot.rcParams["figure.figsize"] = (10,3)
        if self.option_type == 'call':
            pyplot.hist(maximum(S[-1] - self.K, 0), bins=50)
        elif self.option_type == 'put':
            pyplot.hist(maximum(self.K - S[-1], 0), bins=50)
        else:
            print("Give a proper option type")
            
        pyplot.grid(True)
        pyplot.xlabel('option value')
        pyplot.ylabel('frequency')
        pyplot.ylim(0, 7000)
        pyplot.show()
        
       
    def get_option_properties(self):
         super().get_option_properties()
    
    def get_option_payoff(self):
        super().get_option_payoff()
        
        S0, K, r, T, s, option_type = self.S0, self.K, self.r, self.T, self.s, self.option_type
            
        position_type, contract_size, multiplier = self.position_type, self.contract_size, self.multiplier
            
        ceiling = math.ceil(2 * S0) # assuming that the underlying is the same for all the options, we put a limit of the spot price as 2x the current price
        spot_price_table = linspace(0, ceiling, ceiling*10, endpoint=False)  #create the table of spot prices so as to compute the payoff
        payoff = [0]*len(spot_price_table)
        for i in range(0,len(spot_price_table),1):
            if position_type == 'Long':
                payoff[i] = (maximum(spot_price_table[i]-K, 0) * contract_size * multiplier) + payoff[i]
            elif position_type == 'Short':
                payoff[i] = (-maximum(spot_price_table[i]-K,0) * contract_size * multiplier) + payoff[i]
            else: 
                print("Please give either Long or Short for the position type")
            payoff[i] = round(payoff[i],2)
        
        return payoff
    
    # compute the option's VAR and Expected Shortfall using Monte Carlo 
    def get_option_VAR(self):
        
        # Parameters
        S0, K, r, T, s, option_type = self.S0, self.K, self.r, self.T, self.s, self.option_type
       
        M = 1; dt = T / M; I = 10000
        # Simulating I paths with M time steps
        
        S = S0 * exp(cumsum((r - 0.5 * s ** 2) * dt
+ s * math.sqrt(dt)
* random.standard_normal((M + 1, I)), axis=0))
        
        # sum instead of cumsum would also do
        # if only the final values are of interest
        S[0] = S0
       
        # Calculating the Monte Carlo estimator
        
        d1 = (log(S0/K) + (r + (s**2/2))*T)/(s*math.sqrt(T))
        d2 = d1 - (s*math.sqrt(T))
        
        if option_type == 'call':
            option_price = S[-1]*si.norm.cdf(d1, 0.0, 1.0) - K*exp(-r * T)*si.norm.cdf(d2, 0.0, 1.0)
        elif option_type == 'put':
            option_price = K*exp(-r * T)*si.norm.cdf(-d2, 0.0, 1.0) - S[-1]*si.norm.cdf(-d1, 0.0, 1.0)
        else:
            print("Give a proper option type")
        
        pnl = sort(self.price-option_price)
        var = pnl[-500]
            
        print('The European', option_type, 'option price is: ', self.price , 'VAR at 95% C.I. is: ', var )
                
