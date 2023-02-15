#!/usr/bin/env python
# coding: utf-8

# In[5]:


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
    # 'population':18000, 
    # 'oldTakeup': 0.5,
    'ARPU5G': 30,
    'additionalSpending':0.15,
    'subscriberGrowth': 0.04,
    # 'existing_towers_SC': 10,
    # 'existing_towers_MC': 4,
    'discount_rate': 0.04,
    'kind': 'NPV',
    'population_density':36,
}

def NPVEstimate(NPVparams):
    
    # filename = "Peakhour_demand_{}_{}_{}.csv".format(
    #             NPVparams['demand_gb_month'], 
    #             NPVparams['adoption_rate_perc'],
    #             NPVparams['area_covered'],
    #         )
    # my_path = os.path.join('results/DemandPeakHours', filename)
    # df = pd.read_csv(my_path)
    year = np.array([2023,2024,2025,2026,2027,2028,2029,2030,2031,2032])
    population_density = float(NPVparams['population_density'])
    area_covered = int(NPVparams['area_covered'])
    population = population_density*area_covered
    # print(population_density)
    print("File location using os.getcwd():", os.getcwd())
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
    # change = float(NPVparams['change'])
    # kind = params['kind']
    
    
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
    df = pd.DataFrame()
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
            output['strategy'] = np.array(['Solo','Solo','Solo','Solo','Solo','Solo','Solo','Solo','Solo','Solo'])
        elif type == 'PS':
            output['strategy'] = np.array(['Passive','Passive','Passive','Passive','Passive','Passive','Passive','Passive','Passive','Passive'])
        elif type == 'AS':
            output['strategy'] = np.array(['Active','Active','Active','Active','Active','Active','Active','Active','Active','Active'])
        elif type == 'NHN':
            output['strategy'] = np.array(['NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G','NHN5G'])
        # NPVeachYear 
        output['NPVeachYear'] = np.round(np.divide(cashflow,discount_rate))
        # TotalNPV = np.sum(NPVeachYear)
        # output['NPVeachYear']
        
        # arr = np.stack((strategy,year,NPVeachYear), axis = 1)
        filename = "NPVeachYearBaseScenario_{}_{}_{}.csv".format(
            existing_towers_MC, 
            existing_towers_SC,
            type,
        )

        # output = pd.DataFrame(arr,columns=['Scenario','Year','NPVeachYear'])
        if not os.path.exists('results/NPV'):
            os.mkdir('results/NPV')
        my_path = os.path.join('results/NPV', filename)
        output.to_csv(my_path)
    #     df = df.append(output)
    # filename = "NPV_analysis_{}_{}.csv".format(
    #     existing_towers_MC, 
    #     existing_towers_SC,
    # )
    # my_path1 = os.path.join('results/NPV', filename)
    # df.to_csv(my_path1)



#MAin code
NPVEstimate(NPVparams)


def ARPUvariations(NPVparams):
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
    change = np.array([-0.93, -0.66, -0.33,0, 0.33, 0.66, 1])
    
    for change in change:
        ARPU5G = (1+change)*float(NPVparams['ARPU5G'])
        subscriberGrowth = float(NPVparams['subscriberGrowth'])
        additionalSpending = float(NPVparams['additionalSpending'])
        discount_rate = float(NPVparams['discount_rate'])
        # change = float(NPVparams['change'])
        # kind = params['kind']


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
            my_path = os.path.join('results/Cost', filename)
            df = pd.read_csv(my_path)
            arr = df.to_numpy()
            changestr = "NPV"+str(int(change*100))+"ARPU"
            # print(changestr)
            #print(arr)
            TCOPerYear = df["TCO"].to_numpy()
            output['Type'] = np.repeat(changestr,10)
            # arr = df.to_numpy()
            cashflow = np.subtract(totalrevenueperYear,TCOPerYear)
            #print(cashflow)
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

            # output = pd.DataFrame(arr,columns=['Scenario','Year','NPVeachYear'])
            if not os.path.exists('results/NPV/variations'):
                os.mkdir('results/NPV/variations')
            my_path = os.path.join('results/NPV/variations', filename)
            output.to_csv(my_path)



# def combinefiles():
#     my_path = os.path.join('results/NPV/variations', filename)
#     os.chdir("results/NPV/variations")
#     extension = 'csv'
#     all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#     #combine all files in the list
#     combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#     #export to csv
#     combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
    
ARPUvariations(NPVparams)
# combinefiles()

