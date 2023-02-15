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

Demandparams = {
    'demand_gb_month': 50,  
    'adoption_rate_perc': 0.5,
    'area_covered': 500,
}


def demand(Demandparams):
#     """
#     This function estimates the minimum data rate per user required during peak hours to keep the QoE (quality of experience) per user higher.
    
#     """
    DemandperMonth_GB = float(Demandparams['demand_gb_month'])
    #print(DemandperMonth_GB)
    takeuprate = float(Demandparams['adoption_rate_perc'])
    #print(takeuprate)
    AreaCovered_km2 = float(Demandparams['area_covered'])
    
    
    MBperDay_MB = DemandperMonth_GB*math.pow(10,3)/12;
    BusisestHour = 0.15; #overhead booking factor 
    MBperBusyHour_MBphour = MBperDay_MB*BusisestHour;
    MinimumMbpsPerUser_Mbps = MBperBusyHour_MBphour*8/3600; #1 byte = 8 bits and 1 hour = 3600 seconds
    MinimumMbpsPerUser_Mbps = round(MinimumMbpsPerUser_Mbps,2)

    
    randomlist = []
    for i in range(0,24):
        Rc = random.randint(1,50)
        randomlist.append(Rc) 

    output = []
    for RuralPopDensity in range(18,300,18):
        Totalpopulation = AreaCovered_km2*RuralPopDensity;
        TotalUsers = Totalpopulation*takeuprate;
        MinimumSpeedRequiredfortheUsers_Mbps_perkm2 = MinimumMbpsPerUser_Mbps*TotalUsers/AreaCovered_km2;
        MinimumSpeedRequiredfortheUsers_Mbps_perkm2 = round(MinimumSpeedRequiredfortheUsers_Mbps_perkm2,0)
        output.append({
            'iterations': _,
            'PopulationDensity': RuralPopDensity,
            'Totalpopulation': Totalpopulation,
            'TotalUsers_existing': TotalUsers,
            'demand_gb_month': DemandperMonth_GB,
            'adoption_rate_perc':takeuprate,
            'MinimumMbpsPerUser': MinimumMbpsPerUser_Mbps,
            'RequiredDataThroughput': MinimumSpeedRequiredfortheUsers_Mbps_perkm2,
        })

    output = pd.DataFrame(output)
    
    filename = "Peakhour_demand_{}_{}_{}.csv".format(
        Demandparams['demand_gb_month'], 
        Demandparams['adoption_rate_perc'], 
        Demandparams['area_covered'],
    )
    print(filename)
    if not os.path.exists('results/DemandPeakHours'):
            os.mkdir('results/DemandPeakHours')
    my_path = os.path.join('results/DemandPeakHours/', filename)
    print(my_path)
    output.to_csv(my_path)

demand(Demandparams)
# my_path = os.path.join('results/Capacity', filename)


# In[2]:



# import os
 
# print("File location using os.getcwd():", os.getcwd())

