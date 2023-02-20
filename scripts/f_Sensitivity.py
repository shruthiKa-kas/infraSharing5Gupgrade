#!/usr/bin/env python
# coding: utf-8

# In[12]:


import math
import numpy as np
import random
import pandas as pd
import json
import os
import csv

params = {
    'Core_cost_percentage':0.1,
    'backhaul_MC': 10000,
    'backhaul_SC_m': 5,
    'tower': 1000,
    'OPEX_rental': 0.1,
    'opex_small':800,
    'SiteRental_rural_macro': 1000,
    'siteRental_rural_small': 200,
    'cost_RAN_small_USD': 500,
    'carrier_aggregation': 1,
    'power_supply': 250,
    'Control_units':2000,
    'IO_fronthaul': 1500,
    'Remote_radio_units':3500,
    'processing':1500,
    'debt':0.05,
    'CAPEX_rateofChange': -0.03,
    'OPEX_rateofChange': 0.05,
    'Badloans_rateofChange': 0.02,
    'Customer_growth_rate': 0.04,
    'bandwidth_700Mhz': 10,
    'bandwidth_3800MHz':100,
    'cost_spectrum_700_USD': 0.28,
    'cost_spectrum_3800_USD': 0.03,
    'existing_site_density_per_km2': 0.02,
    'coverage_area_km2': 500,
    'population_density':36,
    'backhaul_capacity_Gbps': 5,
    'demand_gb_month': 50,  
    'adoption_rate_perc': 0.5,
    'area_covered': 500,
    'ARPU5G': 30,
    'additionalSpending':0.15,
    'subscriberGrowth': 0.04,
    'discount_rate': 0.04,
    'kind': 'NPV',

}

sensitivityparams = {
    'CAPEX_factor': 1,
    'OPEX_factor': 1,
    'Population_factor': 1,
    'Subscriber_growth_factor': 1,
    'additionalSpending':0.15,
    'Spectrum_factor': 1,
    'Backhaul_factor': 1,
    'Debt_payment_factor': 1,
    'Upgrade_infrastructure_factor': 1,
    'Demand_factor':1,
}

def NPVEstimate(params,sensitivityparams,parameter,j):
    """
    Estimate the cost and NPV for different scenarios in the sentivity analysis
    
    """
    
    population_density = int(params['population_density'])
    '''    
    #initialise params
    '''
    cost_spectrum_700_USD = float(params['cost_spectrum_700_USD'])
    cost_spectrum_3800_USD = float(params['cost_spectrum_3800_USD'])
    bandwidth_700Mhz = float(params['bandwidth_700Mhz']);
    bandwidth_3800MHz = float(params['bandwidth_3800MHz']);
    
    cost_RAN_small_USD = float(params['cost_RAN_small_USD'])
    carrier_aggregation = float(params['carrier_aggregation'])
    power_supply =float(params['power_supply']) 
    control_units = params['Control_units']
    iO_fronthaul = float(params['IO_fronthaul'])
    remote_radio_units = float(params['Remote_radio_units'])
    processing = float(params['processing'])
    core_cost_percentage = float(params['Core_cost_percentage'])
    
    backhaul_MC = params['backhaul_MC']
    backhaul_SC_m = float(params['backhaul_SC_m'])
    tower = float(params['tower'])
    debt = float(params['debt'])
    
    siteRental_rural_macro = float(params['SiteRental_rural_macro'])
    siteRental_rural_small = float(params['siteRental_rural_small'])
    
    OPEX_rental = params['OPEX_rental']
    opex_small = float(params['opex_small'])
    
    CAPEX_rateofChange = float(params['CAPEX_rateofChange'])
    OPEX_rateofchange = float(params['OPEX_rateofChange'])
    Badloans_rateofChange = float(params['Badloans_rateofChange'])
    
    area_covered = int(params['area_covered'])
    ARPU5G = float(params['ARPU5G'])
    subscriberGrowth = float(params['subscriberGrowth'])
    additionalSpending = float(params['additionalSpending'])
    discount_rate = float(params['discount_rate'])
    oldTakeup = float(params['adoption_rate_perc'])
    
    '''
    #initialise senstiviyparams
    '''
    CAPEX_factor = float(sensitivityparams['CAPEX_factor']);
    OPEX_factor = float(sensitivityparams['OPEX_factor']);
    Population_factor = float(sensitivityparams['Population_factor']);
    Subscriber_growth_factor = float(sensitivityparams['Subscriber_growth_factor']);
    Spectrum_factor = float(sensitivityparams['Spectrum_factor']);
    Backhaul_factor = float(sensitivityparams['Backhaul_factor']);
    Debt_payment_factor = float(sensitivityparams['Debt_payment_factor']);
    Upgrade_infrastructure_factor = float(sensitivityparams['Upgrade_infrastructure_factor']);
    Demand_factor = float(sensitivityparams['Demand_factor']);
    
    
    '''
    maincalculations
    
    These equations estimate 
    '''
    year = np.array([2023,2024,2025,2026,2027,2028,2029,2030,2031,2032])
    filename = "Overall_cellrequired_macro_small.csv"
    my_path = os.path.join('data/Capacity', filename)
    df = pd.read_csv(my_path)
    arr = df.to_numpy()
    index = np.where(arr == population_density)
    [iteration, population_density, Number_of_MC_upgrade, Number_of_SC_deployed, overall_towers] = arr[1,:]
    
    existing_towers_SC = Upgrade_infrastructure_factor*int(Number_of_SC_deployed)
    existing_towers_MC = Upgrade_infrastructure_factor*int(Number_of_MC_upgrade)
    
    CAPEX_small = cost_RAN_small_USD*CAPEX_factor;
    CAPEX_macro = CAPEX_factor*(carrier_aggregation+control_units+iO_fronthaul+remote_radio_units+processing);
    CAPEX_rateofChange = np.power((1+CAPEX_rateofChange),(year-2023))
    Core = CAPEX_factor*(core_cost_percentage*(existing_towers_SC*(cost_RAN_small_USD) + existing_towers_MC*(carrier_aggregation+control_units+iO_fronthaul+remote_radio_units+processing)))
    
    siteRental_rural_small = OPEX_factor*siteRental_rural_small
    siteRental_rural_macro = OPEX_factor*siteRental_rural_macro
    OPEX_rateofchange = np.power((1+OPEX_rateofchange),(year-2023))
    OPEX_small = OPEX_factor*(opex_small+power_supply/4)*10;
    OPEX_macro = OPEX_factor*(OPEX_rental*CAPEX_macro+power_supply)*10 ;
    year = np.array([2023,2024,2025,2026,2027,2028,2029,2030,2031,2032])
    
    Badloans_rateofChange = np.power((1+Badloans_rateofChange*Debt_payment_factor),(year-2023))
    population = Population_factor*population_density*area_covered
    initialSubscribers = oldTakeup*population
    upgradeSubscriber = 0.3*initialSubscribers;
    additionalSubscriber = 0.2*population;
    totalSubscriber = upgradeSubscriber + additionalSubscriber

    subscriberGrowth = np.power((1+subscriberGrowth*Subscriber_growth_factor), (year-2023))
    upgradeSubscriber = upgradeSubscriber*subscriberGrowth
    additionalSubscriber = subscriberGrowth*additionalSubscriber
    discount_rate = np.power((1+discount_rate), (year-2023))

    revenueupgradeSubscriber = upgradeSubscriber*additionalSpending*ARPU5G*Demand_factor;
    revenueadditionalSubscriber = additionalSubscriber*ARPU5G*Demand_factor;
    totalrevenueperYear = revenueadditionalSubscriber + revenueupgradeSubscriber;

    change = int((j*100))
    changestr = "change"+str(change)
    
        # output[''] = np.array([])
    Type = np.array(['NS', 'PS', 'AS', 'NHN'])
    output = pd.DataFrame()
    
    def NPVCase(type):    
        # output = []
        # df1 = []
        # output = pd.DataFrame(parameter, columns=['category']) 
        output['category'] = np.array([parameter])
        output['Scenario'] = np.array(changestr)
        if type == 'NS':
            #4 operators scenario
            t = 4; #number of towers upgrade
            b = 4; #number of backhaul upgrade
            s = 4; #number of spectrum upgrade
            r = 4; #number of RAN upgrade
            c = 4; #number of Core upgrade
            output['Type'] = np.array(['Solo'])
        elif type == 'PS':
            t = 1; #number of towers upgrade
            b = 1; #number of backhaul upgrade
            s = 4; #number of spectrum upgrade
            r = 4; #number of RAN upgrade
            c = 4; #number of Core upgrade
            output['Type'] = np.array(['Passive'])
        elif type == 'AS':
            t = 1; #number of towers upgrade
            b = 1; #number of backhaul upgrade
            s = 2; #number of spectrum upgrade
            r = 2; #number of RAN upgrade
            c = 4; #number of Core upgrade
            output['Type'] = np.array(['Active'])
        elif type == 'NHN':
            t = 1; #number of towers upgrade
            b = 1; #number of backhaul upgrade
            s = 1; #number of spectrum upgrade
            r = 1; #number of RAN upgrade
            c = 1; #number of Core upgrade
            output['Type'] = np.array(['NHN5G'])
        
        CAPEX = (((CAPEX_small)*existing_towers_SC*r + siteRental_rural_small*t +  Spectrum_factor*bandwidth_3800MHz*cost_spectrum_3800_USD*population*s + Backhaul_factor*backhaul_SC_m*1000*b) +                     ((CAPEX_macro)*existing_towers_MC*r+ siteRental_rural_macro*t +Core*c + Spectrum_factor*bandwidth_700Mhz*cost_spectrum_700_USD*population*s + Backhaul_factor*backhaul_MC*b))/10*CAPEX_rateofChange
        OPEX =  ((OPEX_small)*existing_towers_SC*r + (OPEX_macro)*existing_towers_MC*r)/10*OPEX_rateofchange
        TCO = CAPEX + OPEX
        Badloans = TCO*Badloans_rateofChange
        TCO_plus_badloans = TCO + Badloans
        
        cashflow = np.subtract(totalrevenueperYear,TCO_plus_badloans)
        output['NPV'] = np.round(np.sum(np.divide(cashflow,discount_rate)))
        return output
    df = pd.DataFrame()   
    df1 = pd.DataFrame()
    for type in Type: 
    # #"Solo", "Passive", "Active", "NHN5G"    
        df = NPVCase(type)
        df1 = df1.append(df)
    
    return df1

            
final = pd.DataFrame()
for i in sensitivityparams.keys():
    parameter = i
    change = np.array([-0.60, -0.40, -0.20, -0.10, 0, 0.10, 0.20, 0.40, 0.60])
    for j in change:
        oldValue = sensitivityparams.get(i)
        sensitivityparams[i] = (1+j)
        a = NPVEstimate(params,sensitivityparams,parameter,j)
        final = final.append(a)
        sensitivityparams[i] = oldValue

filename = "sensitivityAnalysis.csv"
if not os.path.exists('data/Sensitivity'):
    os.mkdir('data/Sensitivity')
my_path = os.path.join('data/Sensitivity', filename)
final.to_csv(my_path)
