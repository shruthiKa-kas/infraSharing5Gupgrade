#!/usr/bin/env python
# coding: utf-8

# In[5]:


"""
Simulation run script for infraSharing5Gupgrade.
Written by Shruthi K A & Ed Oughton.
Jan 2023
"""

import math
import numpy as np
import random
import pandas as pd
import os
from pathlib import Path

demandparams = {
    'demand_gb_month': 50,  
    'adoption_rate_perc': 0.5,
    'area_covered': 500,
}


def demand(demandparams):
    """
    This function estimates the minimum data rate per user required during peak hours to keep the QoE (quality of experience)
    per user higher. 
    Data traffic demand is estimated by determining market share, anticipated smartphone users or other business subscribers,
    population distribution, active users exchanging traffic at peak times, the amount of traffic per user and the amount of 
    traffic per site.

    inputs

        demandperMonth_GB (float): data usage per month of consumer eMBB application
        takeuprate (float): expected network uptake by the consumers in comparison to the total population 
        area_covered_km2 (float): size of the study are in km2

    output

        minimum_speed_required_users_Mbps_perkm2 (float): minimum speed per user during peak hours 

    """
    demandperMonth_GB = float(demandparams['demand_gb_month'])
    takeuprate = float(demandparams['adoption_rate_perc'])
    area_covered_km2 = float(demandparams['area_covered'])
    
    
    MBperDay_MB = demandperMonth_GB*math.pow(10,3) / 12;
    '''
    overhead booking factor 
    '''
    busisest_hour = 0.15; 
    MBperBusyHour_MBphour = MBperDay_MB * busisest_hour;
    minimumMbps_peruser_Mbps = MBperBusyHour_MBphour * 8/ 3600; 
    '''
    1 byte = 8 bits and 1 hour = 3600 seconds
    '''
    minimumMbps_peruser_Mbps = round(minimumMbps_peruser_Mbps,2)

    
    randomlist = []
    for i in range(0,24):
        Rc = random.randint(1,50)
        randomlist.append(Rc) 

    output = []
    for rural_pop_density in range(18,300,18):
        """
        This for loop stimates the minimum data rate per user required during peak hours.
        
        output
            minimum_speed_required_users_Mbps_perkm2 (float): minimum speed per user during peak hours for varying population density.
        """
        
        total_population = area_covered_km2*rural_pop_density;
        total_users = total_population*takeuprate;
        minimum_speed_required_users_Mbps_perkm2 = minimumMbps_peruser_Mbps*total_users/area_covered_km2;
        minimum_speed_required_users_Mbps_perkm2 = round(minimum_speed_required_users_Mbps_perkm2,0)
        output.append({
            'iterations': _,
            'PopulationDensity': rural_pop_density,
            'Totalpopulation': total_population,
            'total_users_existing': total_users,
            'demand_gb_month': demandperMonth_GB,
            'adoption_rate_perc':takeuprate,
            'MinimumMbpsPerUser': minimumMbps_peruser_Mbps,
            'RequiredDataThroughput': minimum_speed_required_users_Mbps_perkm2,
        })

    output = pd.DataFrame(output)
    
    filename = "Peakhour_demand_{}_{}_{}.csv".format(
        demandparams['demand_gb_month'], 
        demandparams['adoption_rate_perc'], 
        demandparams['area_covered'],
    )
    print(filename)
    if not os.path.exists('data/demand_assess'):
            os.mkdir('data/demand_assess')
    my_path = os.path.join('data/demand_assess/', filename)
    print(my_path)
    output.to_csv(my_path)

demand(demandparams)
