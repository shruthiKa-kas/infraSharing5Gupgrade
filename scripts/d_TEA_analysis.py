#!/usr/bin/env python
# coding: utf-8

"""
Simulation run script for infraSharing5Gupgrade.
Written by Shruthi K A & Ed Oughton.
Jan 2023
"""

import math
import numpy as np
import random
import pandas as pd
import json
import os
import glob



#NPV_analysis
NPVparams = {
    'demand_gb_month': 50,  
    'adoption_rate_perc': 0.5,
    'area_covered': 500,
    'ARPU5G': 30,
    'additionalSpending':0.15,
    'subscriberGrowth': 0.04,
    'discount_rate': 0.04,
    'kind': 'NPV',
    'population_density':36,
}

def NPVEstimate(NPVparams):
    '''
    Estimate the NPV of the given cost at the base case parameter values
    '''

    year = np.array([2023,2024,2025,2026,2027,2028,2029,2030,2031,2032])
    population_density = float(NPVparams['population_density'])
    area_covered = int(NPVparams['area_covered'])
    population = population_density*area_covered

    filename = "Overall_cellrequired_macro_small.csv"
    my_path = os.path.join('data/Capacity', filename)
    df = pd.read_csv(my_path)
    arr = df.to_numpy()
    index = np.where(arr == population_density)

    [iteration, population_density, Number_of_MC_upgrade, Number_of_SC_deployed, overall_towers] = arr[1,:]
    existing_towers_SC = int(Number_of_SC_deployed)
    existing_towers_MC = int(Number_of_MC_upgrade)
    
    Type = np.array(['NS', 'PS', 'AS', 'NHN'])
    oldTakeup = float(NPVparams['adoption_rate_perc'])
    
    ARPU5G = float(NPVparams['ARPU5G'])
    subscriberGrowth = float(NPVparams['subscriberGrowth'])
    additionalSpending = float(NPVparams['additionalSpending'])
    discount_rate = float(NPVparams['discount_rate'])
    
    initialSubscribers = oldTakeup*population
    upgradeSubscriber = 0.3*initialSubscribers;
    additionalSubscriber = 0.2*initialSubscribers;
    totalSubscriber = upgradeSubscriber + additionalSubscriber
    
    '''
    Consider the future growth in the subscribers
    '''
    
    subscriberGrowth = np.power((1+subscriberGrowth), (year-2023))
    upgradeSubscriber = upgradeSubscriber*subscriberGrowth
    additionalSubscriber = subscriberGrowth*additionalSubscriber
    discount_rate = np.power((1+discount_rate), (year-2023))
    
    revenueupgradeSubscriber = upgradeSubscriber*additionalSpending*ARPU5G;
    revenueadditionalSubscriber = additionalSubscriber*ARPU5G;
    totalrevenueperYear = revenueadditionalSubscriber + revenueupgradeSubscriber;
    df = pd.DataFrame()
    output = pd.DataFrame(year, columns=['year']) 
    for type in Type:
        filename = "cost_{}_{}_{}.csv".format(
                existing_towers_MC, 
                existing_towers_SC,
                type,
            )
        my_path = os.path.join('data/Cost', filename)
        df = pd.read_csv(my_path)
        arr = df.to_numpy()
        TCOPerYear = df["TCO"].to_numpy()
        cashflow = np.subtract(totalrevenueperYear,TCOPerYear)
        if type == 'NS':
            output['strategy'] = np.array(['Solo','Solo','Solo','Solo','Solo','Solo','Solo','Solo','Solo','Solo'])
        elif type == 'PS':
            output['strategy'] = np.array(['Passive','Passive','Passive','Passive','Passive','Passive','Passive','Passive','Passive','Passive'])
        elif type == 'AS':
            output['strategy'] = np.array(['Active','Active','Active','Active','Active','Active','Active','Active','Active','Active'])
        elif type == 'NHN':
            output['strategy'] = np.array(['NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G'])

        output['NPVeachYear'] = np.round(np.divide(cashflow,discount_rate))
        filename = "NPVeachYearBaseScenario_{}_{}_{}.csv".format(
            existing_towers_MC, 
            existing_towers_SC,
            type,
        )


        if not os.path.exists('data/NPV'):
            os.mkdir('data/NPV')
        my_path = os.path.join('data/NPV', filename)
        output.to_csv(my_path)





def ARPUvariations(NPVparams):
    
    '''
    Estimate the NPV of the given cost by varying the base case parameter values by -93% to +100%, to study the impact of revenue
    on the network feasibility using different infrastructure sharing strategies.
    '''
    
    year = np.array([2023,2024,2025,2026,2027,2028,2029,2030,2031,2032])
    population_density = float(NPVparams['population_density'])
    area_covered = int(NPVparams['area_covered'])
    population = population_density*area_covered
    filename = "Overall_cellrequired_macro_small.csv"
    my_path = os.path.join('data/Capacity', filename)
    df = pd.read_csv(my_path)
    arr = df.to_numpy()
    index = np.where(arr == population_density)

    [iteration, population_density, Number_of_MC_upgrade, Number_of_SC_deployed, overall_towers] = arr[1,:]
    existing_towers_SC = int(Number_of_SC_deployed)
    existing_towers_MC = int(Number_of_MC_upgrade)
    
    Type = np.array(['NS', 'PS', 'AS', 'NHN'])
    oldTakeup = float(NPVparams['adoption_rate_perc'])

    change = np.array([-0.93, -0.66, -0.33,0, 0.33, 0.66, 1])
    
    for change in change:
        ARPU5G = (1+change)*float(NPVparams['ARPU5G'])
        subscriberGrowth = float(NPVparams['subscriberGrowth'])
        additionalSpending = float(NPVparams['additionalSpending'])
        discount_rate = float(NPVparams['discount_rate'])

        initialSubscribers = oldTakeup*population
        upgradeSubscriber = 0.3*initialSubscribers;
        additionalSubscriber = 0.2*population;
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
            my_path = os.path.join('data/Cost', filename)
            df = pd.read_csv(my_path)
            arr = df.to_numpy()
            changestr = "NPV"+str(int(change*100))+"ARPU"
            TCOPerYear = df["TCO"].to_numpy()
            output['Type'] = np.repeat(changestr,10)
            cashflow = np.subtract(totalrevenueperYear,TCOPerYear)
            if type == 'NS':
                output['Scenario'] = np.array(['Solo','Solo','Solo','Solo','Solo','Solo','Solo','Solo','Solo','Solo'])
            elif type == 'PS':
                output['Scenario'] = np.array(['Passive','Passive','Passive','Passive','Passive','Passive','Passive','Passive','Passive','Passive'])
            elif type == 'AS':
                output['Scenario'] = np.array(['Active','Active','Active','Active','Active','Active','Active','Active','Active','Active'])
            elif type == 'NHN':
                output['Scenario'] = np.array(['NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G'])
            # NPVeachYear 
            output['NPVeachYear'] = np.round(np.divide(cashflow,discount_rate))

            filename = "NPVeachYear_ARPU_{}_{}_{}_{}.csv".format(
                existing_towers_MC, 
                existing_towers_SC,
                type,
                change,
            )

            if not os.path.exists('data/NPV/variations'):
                os.mkdir('data/NPV/variations')
            my_path = os.path.join('data/NPV/variations', filename)
            output.to_csv(my_path)

'''
Main code
'''
NPVEstimate(NPVparams)
ARPUvariations(NPVparams)


