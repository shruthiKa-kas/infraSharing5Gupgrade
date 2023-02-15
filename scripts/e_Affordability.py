#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import required libraries
import numpy as np
from scipy.optimize import linprog

# Set the inequality constraints matrix
# Note: the inequality constraints must be in the form of <=
A = np.array([[-1, -1, -1], [-1, 2, 0], [0, 0, -1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]])

# Set the inequality constraints vector
b = np.array([-1000, 0, -340, 0, 0, 0])

# Set the coefficients of the linear objective function vector
c = np.array([10, 15, 25])

# Solve linear programming problem
res = linprog(c, A_ub=A, b_ub=b)

# Print results
print('Optimal value:', round(res.fun, ndigits=2),
      '\nx values:', res.x,
      '\nNumber of iterations performed:', res.nit,
      '\nStatus:', res.message)


# In[3]:


import math
import numpy as np
import random
import pandas as pd
import json
import os
# import ipynb.fs.full.cost_assessment 
from scipy.optimize import linprog

NPVparams = {
    'demand_gb_month': 50,  
    'adoption_rate_perc': 0.5,
    'area_covered': 500,
    'ARPU5G': 30,
    'additionalSpending':0.15,
    'subscriberGrowth': 0.04,
    'discount_rate': 0.02,
    'kind': 'NPV',
    'population_density':36,
}

def NPVEstimate(NPVparams):
    
    year = np.array([2023,2024,2025,2026,2027,2028,2029,2030,2031,2032])
    population_density = float(NPVparams['population_density'])
    area_covered = int(NPVparams['area_covered'])
    population = population_density*area_covered
    # print(population_density)
    filename = "Overall_cellrequired_macro_small.csv"
    my_path = os.path.join('results/Capacity', filename)
    df = pd.read_csv(my_path)
    # print(df)
    arr = df.to_numpy()
    # print(arr[1,:])
    index = np.where(arr == population_density)
    # print(index)
    [iteration, population_density, Number_of_MC_upgrade, Number_of_SC_deployed, overall_towers] = arr[1,:]
    existing_towers_SC = int(Number_of_SC_deployed)
    existing_towers_MC = int(Number_of_MC_upgrade)
    
    Type = np.array(['NS', 'PS', 'AS', 'NHN'])
    oldTakeup = float(NPVparams['adoption_rate_perc'])
    # population = float(params['population'])
    
    ARPU5G = float(NPVparams['ARPU5G'])
    subscriberGrowth = float(NPVparams['subscriberGrowth'])
    additionalSpending = float(NPVparams['additionalSpending'])
    discount_rate = float(NPVparams['discount_rate'])
    
    initialSubscribers = oldTakeup*population
    upgradeSubscriber = 0.3*initialSubscribers;
    additionalSubscriber = 0.2*initialSubscribers;
    totalSubscriber = upgradeSubscriber + additionalSubscriber
    
    subscriberGrowth = np.power((1+subscriberGrowth), (year-2023))
    upgradeSubscriber = upgradeSubscriber*subscriberGrowth
    additionalSubscriber = subscriberGrowth*additionalSubscriber
    discount_rate = np.power((1+discount_rate), (year-2023))
    
    revenueupgradeSubscriber = upgradeSubscriber*additionalSpending*ARPU5G;
    revenueadditionalSubscriber = additionalSubscriber*ARPU5G;
    totalrevenueperYear = revenueadditionalSubscriber + revenueupgradeSubscriber;
    
    output = pd.DataFrame(year, columns=['year']) 
    for type in Type:
        filename = "cost_{}_{}_{}.csv".format(
                existing_towers_MC, 
                existing_towers_SC,
                type,
            )
        my_path = os.path.join('results/Cost', filename)
        df = pd.read_csv(my_path)
        arr = df.to_numpy()
        #print(arr)
        TCOPerYear = df["TCO"].to_numpy()
        # arr = df.to_numpy()
        cashflow = np.subtract(totalrevenueperYear,TCOPerYear)
        #print(cashflow)
        if type == 'NS':
            output['strategy'] = np.array(['Solo'])
        elif type == 'PS':
            output['strategy'] = np.array(['Passive'])
        elif type == 'AS':
            output['strategy'] = np.array(['Active'])
        elif type == 'NHN':
            output['strategy'] = np.array(['NHN5G'])
        # NPVeachYear 
        output['NPV'] = np.sum(np.round(np.divide(cashflow,discount_rate)))
        

        # output = pd.DataFrame(arr,columns=['Scenario','Year','NPVeachYear'])
        if not os.path.exists('results/NPV'):
            os.mkdir('results/NPV')
        my_path = os.path.join('results/NPV', filename)
        output.to_csv(my_path)
        



#MAin code
NPVEstimate(NPVparams)

