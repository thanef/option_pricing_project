from numpy import *
import math
from matplotlib import pyplot

class Portfolio:
    
    def __init__(self, name):
        self.name = name
        self.product_list = []
        self.premium = 0

    def add_product(self, product):
        self.product_list.append(product)
        
    # Method that calculates the premium required for the portfolio after adding up all the products
    def calculate_premium_strategy(self):
        premium = 0
        for product in self.product_list:
            if product.position_type == 'Long':
                premium = premium - (product.price * product.contract_size * product.multiplier)
            elif product.position_type == 'Short':
                premium = premium + (product.price * product.contract_size * product.multiplier)
            else: 
                print("Please give either Long or Short for the position type")
        print('The premium for the strategy stands at: ', round(premium,2), ' Euros')
        self.premium = premium

    # Method that calculates the payoff for different spot prices and generates the relevant option's strategy graph
    def calculate_payoff_strategy(self):
        
        ceiling = math.ceil(2 * self.product_list[0].S0) # assuming that the underlying is the same for all the options, we put a limit of the spot price as 2x the current price
        spot_price_table = linspace(0, ceiling, ceiling*10, endpoint=False)  #create the table of spot prices so as to compute the payoff
        
        payoff = [0]*len(spot_price_table)
        for product in self.product_list:
            payoff = list( map(add, payoff, product.payoff) )
            
        payoff = payoff + self.premium
        
        # Graph showing the option strategy
        pyplot.title(self.name)
        pyplot.plot(spot_price_table, payoff)
        pyplot.grid(True)
        pyplot.xlabel('Price of the Underlying')
        pyplot.ylabel('Profit & Loss')
        pyplot.show()
                    
                    
     


                
            