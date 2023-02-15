#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""
Simulation run script for infraSharing5Gupgrade.
Written by Shruthi K A & Ed Oughton.
Jan 2023
"""

import numpy as np
import math
import pandas as pd
import random
import os
# from ipynb.fs.full.CostAssessment import costEstimate
import ipynb.fs.full.b1_capacity_assessment
# from ipynb.fs.full.demand_assessment import Demandparams

#dataschedulling - exported from 5G NR planning and extended to suit this study
# Author: Zulfadli Zainal
# Github: https://github.com/zulfadlizainal
# Linkedin: https://linkedin.com/in/zulfadlizainal


SchedulePramas = {
    'demand_gb_month': 50,  
    'adoption_rate_perc': 0.5,
    'area_covered': 500,
    'subscriber_growth': 0.04,
    'duration': 10,
    'Bandwidth_MHz': 10,
    'Frequency_MHz': 700,
    'FrequencySpacing_KHz': 15,
    'pentration_5G': 0.5,
}

#data scheduling requests
def dataScheduling():
    type = 'Data';

    dl_act_factor = 30/100         # Unit: %
    ul_act_factor = 10/100         # Unit: %

    mo_avgrrcuser_nbh = 5          # Unit: Avg RRC User / UE / Hour
    mt_avgrrcuser_nbh = 2          # Unit: Avg RRC User / UE / Hour

    sch_periodicity = 4                          # Unit: ms
    sch_periodicity_frame = 10/sch_periodicity   # Unit: ms

    bler = 10/100                   # Unit %

    short_user_duration = 20/3600   # Unit: s/3600 (Erlang)
    mid_user_duration = 60/3600     # Unit: s/3600 (Erlang)
    long_user_duration = 300/3600   # Unit: s/3600 (Erlang)

    # Calculations

    subscribers = list(range(0, 100, 10))

    df_subs = pd.DataFrame(subscribers, columns=['Subscribers'])

    df_subs['Short_User'] = df_subs['Subscribers']*[short_user_duration]*[dl_act_factor +
                                                                                   ul_act_factor]*[mo_avgrrcuser_nbh+mt_avgrrcuser_nbh]*[sch_periodicity_frame]*[1+bler]
    df_subs['Mid_User'] = df_subs['Subscribers']*[mid_user_duration]*[dl_act_factor +
                                                                               ul_act_factor]*[mo_avgrrcuser_nbh+mt_avgrrcuser_nbh]*[sch_periodicity_frame]*[1+bler]
    df_subs['Long_User'] = df_subs['Subscribers']*[long_user_duration]*[dl_act_factor +
                                                                                  ul_act_factor]*[mo_avgrrcuser_nbh+mt_avgrrcuser_nbh]*[sch_periodicity_frame]*[1+bler]

    output = pd.DataFrame(df_subs)
    filename = "Scheduling_Calculator_{}.csv".format(
            type,
        )
    if not os.path.exists('results/Capacity'):
        os.mkdir('results/Capacity')
    my_path = os.path.join('results/Capacity', filename)
    output.to_csv(my_path, index=False)   

    
#voice scheduling requests
def voicescheduling():
    # Assumptions
    type = 'Voice';
    voice_act_factor = 60/100           # Unit: %

    mo_call_nbh = 1                     # Unit: Call / UE / Hour
    mt_call_nbh = 1                     # Unit: Call / UE / Hour

    voice_packet_periodicity = 20                                # Unit: ms
    voice_periodicity_frame = 10/voice_packet_periodicity        # Unit: ms

    bler = 5/100                        # Unit %

    short_user_duration = 20/3600       # Unit: s/3600 (Erlang)
    mid_user_duration = 60/3600         # Unit: s/3600 (Erlang)
    long_user_duration = 300/3600       # Unit: s/3600 (Erlang)

    # Calculations

    subscribers = list(range(0, 100, 10))

    df_subs = pd.DataFrame(subscribers, columns=['Subscribers'])

    df_subs['Short User (20 Sec)'] = df_subs['Subscribers']*[short_user_duration] *         [voice_act_factor]*[mo_call_nbh+mt_call_nbh] *         [voice_periodicity_frame]*[1+bler]
    df_subs['Mid User (60 Sec)'] = df_subs['Subscribers']*[mid_user_duration] *         [voice_act_factor]*[mo_call_nbh+mt_call_nbh] *         [voice_periodicity_frame]*[1+bler]
    df_subs['Long User (300 Sec)'] = df_subs['Subscribers']*[long_user_duration] *         [voice_act_factor]*[mo_call_nbh+mt_call_nbh] *         [voice_periodicity_frame]*[1+bler]
    
    output = pd.DataFrame(df_subs)
    filename = "Scheduling_Calculator_{}.csv".format(
            type,
        )
    if not os.path.exists('results/Capacity'):
        os.mkdir('results/Capacity')
    my_path = os.path.join('results/Capacity', filename)
    output.to_csv(my_path, index=False) 
    
    
def initialparamters(SchedulePramas):
    subscriber_growth = float(SchedulePramas['subscriber_growth'])
    duration = float(SchedulePramas['duration'])
    area_covered = float(SchedulePramas['area_covered']) 
    Bandwidth_MHz = float(SchedulePramas['Bandwidth_MHz'])
    fc_MHz = float(SchedulePramas['Frequency_MHz'])
    FrequencySpacing_KHz = float(SchedulePramas['FrequencySpacing_KHz'])
    pentration_5G = float(SchedulePramas['pentration_5G'])
    # a = np.arange(3)
    # for a in a:
    #     SchedulePramas['demand_gb_month'] = Demandparams['demand_gb_month']
    #     SchedulePramas['adoption_rate_perc'] = Demandparams['adoption_rate_perc']
    #     SchedulePramas['area_covered'] = Demandparams['area_covered']
    
    filename = "Peakhour_demand_{}_{}_{}.csv".format(
                SchedulePramas['demand_gb_month'], 
                SchedulePramas['adoption_rate_perc'],
                SchedulePramas['area_covered'],
            )
    my_path = os.path.join('results/DemandPeakHours', filename)
    df = pd.read_csv(my_path)
    MinSpeedPerUser = df['MinimumMbpsPerUser'].to_numpy()
    population_desnity = df['PopulationDensity'].to_numpy()
    total_population = population_desnity*area_covered
    users = df['TotalUsers_existing'].to_numpy()
    # print(MinSpeedPerUser[0])
    x = len(users)
    x = np.arange(x)
    #AF = 0.6, voice: AF = 1, data
    
    # traffic_valume = traffic_erlang*3600*BearerBR*AF 
    users_future = users*math.pow((1+subscriber_growth),duration)
    
    #number of users using 5G (50% of overall users)
    users_future_5G = pentration_5G*users_future
    
    return users,users_future_5G,users_future,x,fc_MHz,MinSpeedPerUser,population_desnity,total_population,Bandwidth_MHz,FrequencySpacing_KHz,area_covered
    
    
def trafficpredictions():
    [users,users_future_5G,users_future,x,fc_MHz,MinSpeedPerUser,population_desnity,total_population,Bandwidth_MHz,FrequencySpacing_KHz,area_covered] = initialparamters(SchedulePramas)
    if fc_MHz == 700:
        Current_total_traffic_offered_Mbps = users*MinSpeedPerUser
    elif fc_MHz == 3800:
        Current_total_traffic_offered_Mbps = users*MinSpeedPerUser*15 
    if fc_MHz == 700:
        total_traffic_offered_Mbps = users_future_5G*MinSpeedPerUser
    elif fc_MHz == 3800:
        total_traffic_offered_Mbps = users_future_5G*MinSpeedPerUser*15
            
    # print(total_traffic_offered_Mbps)
    
    #calculate cell by capacity
#     'Bandwidth_MHz': 10,
    # 'Frequency_MHz': 700,
    # 'FrequencySpacing_KHz': 15,
    filename = "capacityCalculator_{}_{}_{}.csv".format(
                SchedulePramas['Bandwidth_MHz'], 
                SchedulePramas['Frequency_MHz'],
                SchedulePramas['FrequencySpacing_KHz'],
            )
    my_path = os.path.join('results/Capacity', filename)
    df = pd.read_csv(my_path)
    cell_capacity_each_sector = df['usable_dataRates_Mbps'].to_numpy()
    # users = df['TotalUsers'].to_numpy()
    # cell_capacity_each_sector = 
    gNodeB_capacity = 3*cell_capacity_each_sector
    
    congestion_control = 0.2; #20% of throughput is used to manage the congestion
    current_number_of_sites = Current_total_traffic_offered_Mbps/gNodeB_capacity
    current_number_of_sites = np.round(current_number_of_sites+1)
    number_of_sites = total_traffic_offered_Mbps/gNodeB_capacity
    number_of_sites = np.round_(number_of_sites+1)
    print(np.round_(number_of_sites+1),0)
    
    output = []
    filename = "TrafficScheduler_cellrequired_{}_{}_{}.csv".format(
            SchedulePramas['Bandwidth_MHz'], 
            SchedulePramas['Frequency_MHz'],
            SchedulePramas['FrequencySpacing_KHz'],
        )
   
    for i in x:
        output.append({
            'population':total_population[i],
            'current_users':users[i],
            'users_on_5G': users_future[i], 
            'Bandwidth_MHz':Bandwidth_MHz,
            'Frequency_MHz':fc_MHz,
            'FrequencySpacing_KHz':FrequencySpacing_KHz,
            'total_traffic_offered_Mbps':total_traffic_offered_Mbps[i],
            'current_number_of_sites_for_upgrade': current_number_of_sites[i],
            'future_number_of_sites_for_upgrade':number_of_sites[i],
                       })
        
    output = pd.DataFrame(output)
    
    if not os.path.exists('results/Capacity'):
        os.mkdir('results/Capacity')
    my_path = os.path.join('results/Capacity', filename)
    output.to_csv(my_path)
    
    #capacity radius Estimation from link budget
    filename = "cell_radius_Calculator_{}_{}_{}.csv".format(
                SchedulePramas['Bandwidth_MHz'], 
                SchedulePramas['Frequency_MHz'],
                SchedulePramas['FrequencySpacing_KHz'],
            )
    my_path = os.path.join('results/Capacity', filename)
    df1 = pd.read_csv(my_path)
    cell_radius_m = df1['cell_radius_m'].to_numpy()
    #print(cell_radius_m)
    area_per_cell = 1.95*2.6*math.pow(cell_radius_m/1000,2)
    TotalCellSite_for_upgrade_capacity = area_covered/area_per_cell
    TotalCellSite_for_upgrade_capacity = np.round_(TotalCellSite_for_upgrade_capacity+1)
    # print(TotalCellSite_for_upgrade_capacity)
    
    #select the maximum sites required
    TotalCellSite_for_upgrade = []
    for i in x:
        TotalCellSite_for_upgrade.append(max(number_of_sites[i], TotalCellSite_for_upgrade_capacity))
        # steps = np.append(steps, step, axis=0)
        # for i in range(5,11):
        #     numbers.append(10*i)
        
 
    return TotalCellSite_for_upgrade, population_desnity 
    

def towersSufficient(overall_towers,SchedulePramas):
    [users,users_future_5G,users_future,x,fc_MHz,MinSpeedPerUser,population_desnity,total_population,Bandwidth_MHz,FrequencySpacing_KHz,area_covered] = initialparamters(SchedulePramas)
    users_per_tower = users_future_5G/overall_towers
    users_per_sector =  users_per_tower/3
    avg_active_subscribers = 0.25*users_per_sector
    for i in x:
        if(avg_active_subscribers[i] < 60):
            print('sufficient upgrade')
        else:
            print('upgrade insufficient')
    

#Main function    
voicescheduling()
dataScheduling()

a = np.array([0,1])

overall_towers = 0
TotalCellSite_for_upgrade_capacity1 = []
TotalCellSite_for_upgrade_capacity2 = []
for a in a:
    if a == 0:
        [TotalCellSite_for_upgrade1, population_desnity] = trafficpredictions()
        # print(TotalCellSite_for_upgrade1,TotalCellSite_for_upgrade1)
    if a == 1:
        SchedulePramas['Frequency_MHz'] = 3800
        SchedulePramas['Bandwidth_MHz'] = 100        
        [TotalCellSite_for_upgrade2, population_desnity] = trafficpredictions()
        overall_towers = np.add(TotalCellSite_for_upgrade1,TotalCellSite_for_upgrade2)
        print(overall_towers)
    
        x = len(population_desnity)
        x = np.arange(x)
        # for i in x:
        #     population_desnity[i] = population_desnity[i]
        #     TotalCellSite_for_upgrade_macro = TotalCellSite_for_upgrade1[i]
        #     TotalCellSite_for_upgrade_small = TotalCellSite_for_upgrade2[i]
        output = pd.DataFrame(population_desnity, columns=['population_desnity'])    
        output['Number_of_macro_cells'] = TotalCellSite_for_upgrade1
        output['Number_of_small_cells'] = TotalCellSite_for_upgrade2
        output['overall_towers'] = overall_towers

        # for i in x:
        #     output = np.concatenate((population_desnity,TotalCellSite_for_upgrade_capacity1,TotalCellSite_for_upgrade_capacity2))
        #     # output.append([output])
        # #, columns=['Population_density', 'Number_of_macro_cells', 'Number_of_small_cells'])
        # for i in x:
        #     a = np.concatenate([population_desnity[i],TotalCellSite_for_upgrade_capacity1[i]], axis=1)
        #     b = np.concatenate([population_desnity[i],TotalCellSite_for_upgrade_capacity2[i]],axis=1)

        filename = "Overall_cellrequired_macro_small.csv"
        # filename1 = "Overall_cellrequired_macro.csv"
        # for i in x:
        #     output.append({
        #         'number_of_macro_cells_upgrade':TotalCellSite_for_upgrade_capacity1[i],
        #         'number_of_small_cells_deployed':TotalCellSite_for_upgrade_capacity2[i],
        #         'population_desnity':population_desnity[i],
        #                    })

        output = pd.DataFrame(output)
        # output1 = pd.DataFrame(b)

        if not os.path.exists('results/Capacity'):
            os.mkdir('results/Capacity')
        my_path = os.path.join('results/Capacity', filename)
        # my_path1 = os.path.join('results/Capacity',filename2)
        output.to_csv(my_path)
        # output1.to_csv(my_path1)
        # , columns=['population_desnity', 'Number_of_small_cells']
        # , columns=['population_desnity', 'Number_of_macro_cells']
    
towersSufficient(overall_towers,SchedulePramas)


# In[ ]:




