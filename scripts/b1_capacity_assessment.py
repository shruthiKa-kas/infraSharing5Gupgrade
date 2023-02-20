#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

params = {
    'MIMO_up': 4,
    'MIMO_down': 4,
    'MUMIMO_number_of_beams': 8,
    'Mode_of_Modulation_and_Code_Rate': 28,
    'modulation_order': 50,
    'TargetcodeRate': 948,
    'Scaling_factor': 1,
    'Mode': 'TDD',
    'Bandwidth_MHz': 10,
    'Frequency_MHz': 700,
    'FrequencySpacing_KHz': 15,
    'overhead': 0.14,
    'Part_of_slots_DL_TDD': 0.7,
    'demand_gb_month': 50,
    'adoption_rate_perc': 50,
    'cell_radius': 10,
    'mimo_layers': 4,
    'beamforming_mmimo': 'yes',
    'mu_mimo_beams': 10,
    'scaling_factor': 1,
    'carrier_aggregation': 1,
    'direction_of_link': 'DL',
    'Max_Tx_Power_dB': 40,
    'number_of_antennas': 16,
    'antenna_Gain_dB': 16,
    'cable_loss_dB': 2,
    'height_gNodeB': 40,
    'type_of_coverage': 'LOS',
    'antennaGain_rx': 1,
    'utnoise_figure': 4,
    'targetSINR': 5,
    'cable_loss_rx': 0,
    'height_UT': 1.5, 
    'coverageLoc': 'Outdoor',
    'number_of_walls':1,
    'depth_of_wall':1,
    'SlowFadingMargin_dB': 7,
    'standarddeviationRural':6,  
    'confidenceInterval': 0.95,
}


def capacity(params):
    '''
    Сalculator allows to calculate the maximum throughput of 5G NR network for user (depending on his mobile device UE) or cell. 
    Approximately data transfer rate of 5G NR can be calculated using the formula:
    3GPP specifications TS 38.306 shares a formula for calculating the maximum data rate that a UE/cell can support in downlink and uplink. 
    v(j)Layers - maximum number of MIMO layers ,3GPP 38.802: maximum 8 in DL, maximum 4 in UL
    '''
    v= float(params['MIMO_down']);
    '''
    nbeam = 1, minimum
    '''
    nbeam = float(params['MUMIMO_number_of_beams']);
    '''
    Mode of Modulation and Code Rate:
        '''
    MCS = float(params['Mode_of_Modulation_and_Code_Rate']);
    '''
    Q(j)m modulation order (3GPP 38.804, 38.214)
    '''
    Qjm = 6;
    '''#For UL and DL Q(j)m is same (QPSK-2, 16QAM-4, 64QAM-6, 256QAM-8, 1024QAM-10)'''
    TargetcodeRate = float(params['TargetcodeRate']);                  
    Rmax = TargetcodeRate/1024;    
    '''
    f(j) Scaling factor (3GPP 38.306) = 1,0.8,0.75,0.4
    '''
    f = float(params['Scaling_factor']);
    '''
    BW(j)- band Bandwidth, MHz (3GPP 38.104)
    '''
    Bandwidth_MHz = float(params['Bandwidth_MHz']);
    Mode = params['Mode'];            
    Frequency_MHz = float(params['Frequency_MHz']); 
    FrequencySpacing_KHz = float(params['FrequencySpacing_KHz']);
    '''
    Overhead OH(j) for control channels Mode
    '''
    OH = float(params['overhead']); 
    '''
    NbwPRB, maximum number of PRB (3GPP 38.104) for selected BW(j), FR(j), µ(j)
    '''
    NbwPRB = float(math.floor(Bandwidth_MHz*1000/(FrequencySpacing_KHz*12)))-3;
    
    
    if Mode == 'TDD': 
        if Frequency_MHz == 700:
              carrieraggregation = 0;
              '''
              Part of the Slots allocated for DL in TDD mode, 1= 100% slot usage
              '''
              T = float(params['Part_of_slots_DL_TDD']); 
        else:
              carrieraggregation = 1;
              '''
              Part of the Slots allocated for DL in FDD mode, 1= 100% slot usage
              '''
              T = 1;
    else:
        carrieraggregation = 1;  
        T = 1; '''F-OFDM''' 
    if FrequencySpacing_KHz == 15:
        mu = 0;
        MaxRB = 270;
        if NbwPRB > MaxRB:
            NbwPRB = MaxRB;
    elif FrequencySpacing_KHz == 30:
        mu = 1;
        MaxRB = 273;
        if NbwPRB > MaxRB:
            NbwPRB = MaxRB;
    else:
        mu = 2;
        MaxRB = 135;
        if NbwPRB > MaxRB:
            NbwPRB = MaxRB;
    print(type(NbwPRB),NbwPRB, 'NbwPRB')
    
    '''3GPP 38.101 has specified maximum transmission bandwidth configuration for each UE channel and sub-carrier spacing provided in below table. 
    The resource block number shown are after removing guard band from channel bandwidth and maximum bandwidth considered is 100 MHz'''
    GuardBand = float(0.5*Bandwidth_MHz*1000 - (0.5*FrequencySpacing_KHz*12*NbwPRB) - 0.5*FrequencySpacing_KHz);
    print(GuardBand, 'Guard Band (KHz)')
    
    OneRB_size_frequencyDomain_KHz = FrequencySpacing_KHz*12; 
    '''
    In 5G, One NR Resource Block (RB) contains 12 sub-carriers in frequency domain similar to LTE.
    In LTE resource block bandwidth is fixed to 180 KHz but in NR it is not fixed and depend on sub-carrier spacing.
    '''
    OneRB_size_TimeDomain_ms = 1/math.pow(2,mu);
    Ts = 1/(1000*14*math.pow(2,mu))             
    dataRates_Mbps = math.pow(10,-6)*v*Qjm*f*Rmax*NbwPRB*12*(1-OH)/Ts*nbeam;  
    usable_dataRates_Mbps = dataRates_Mbps*T;
    print(OneRB_size_frequencyDomain_KHz, 'OneRB_size_frequencyDomain_KHz')
    print(OneRB_size_TimeDomain_ms, 'OneRB_size_TimeDomain_ms')
    print(Mode, 'Data Rates (Mbps)',dataRates_Mbps)             
    print(Mode, 'Usable Data Rates (Mbps)', usable_dataRates_Mbps)
    
    ''' 
    To determine a cell’s overall practical capacity for broadband, and thus to evaluate the real capability of any proposed network that leverages wireless
    technology, one must consider the average of the experience among all users near and far. This is often only 15–25 percent of the theoretical peak for a 
    single user. When overheads are considered, the usable capacity will typically be less than 75 percent of this value. It therefore is not unusual for 
    the actual throughput capacity to be only roughly 15 percent of its peak data connection rate – although the latter is the speed that is usually promoted.
    '''
    ActualCapacity_Mbps = 0.15*usable_dataRates_Mbps;
    print('Actual average Capacity_Mbps', ActualCapacity_Mbps)
    output = []
    filename = "capacityCalculator_{}_{}_{}.csv".format(
            params['Bandwidth_MHz'], 
            params['Frequency_MHz'],
            params['FrequencySpacing_KHz'],
        )
    
    output.append({
        'dataRates_Mbps': dataRates_Mbps, 
        'Bandwidth_MHz':Bandwidth_MHz,
        'Frequency_MHz':Frequency_MHz,
        'FrequencySpacing_KHz':FrequencySpacing_KHz,
        'usable_dataRates_Mbps':usable_dataRates_Mbps,
        'ActualCapacity_Mbps':ActualCapacity_Mbps,
                   })
    output = pd.DataFrame(output)
    if not os.path.exists('data/Capacity'):
        os.mkdir('data/Capacity')
    my_path = os.path.join('data/Capacity', filename)
    output.to_csv(my_path)

def maximumAllowablePathLoss(params):
    fc_MHz = float(params['Frequency_MHz'])
    Bandwidth_MHz = float(params['Bandwidth_MHz'])
    FrequencySpacing_KHz = float(params['FrequencySpacing_KHz'])
    ThermalNoise_dB = -174 + 10*math.log10(Bandwidth_MHz*math.pow(10,6))
    NbwPRB = float(math.floor(Bandwidth_MHz*1000/(FrequencySpacing_KHz*12)))-3;
    if FrequencySpacing_KHz == 15:
        mu = 0;
        MaxRB = 270;
        if NbwPRB > MaxRB:
            NbwPRB = MaxRB;
    elif FrequencySpacing_KHz == 30:
        mu = 1;
        MaxRB = 273;
        if NbwPRB > MaxRB:
            NbwPRB = MaxRB;
    else:
        mu = 2;
        MaxRB = 135;
        if NbwPRB > MaxRB:
            NbwPRB = MaxRB;
    print(type(NbwPRB),NbwPRB, 'NbwPRB')
    SubcarrierQuantity = NbwPRB*12
    '''
    gNodeB configuration
    '''
    Max_Tx_Power = float(params['Max_Tx_Power_dB'])
    No_Antennas = float(params['number_of_antennas'])
    Reference_singal_power_dBm = Max_Tx_Power - 10*math.log10(NbwPRB*12)
    Total_transmit_power_dBm = Max_Tx_Power + 10*math.log10(No_Antennas)
    print(Reference_singal_power_dBm, 'Reference_singal_power_dBm')
    print(Total_transmit_power_dBm, 'Total_transmit_power_dBm')

    TxperPRB = Total_transmit_power_dBm/NbwPRB
    AntennaGain_Tx = float(params['antenna_Gain_dB']);
    CableLoss_Tx = float(params['cable_loss_dB']);
    hBS = float(params['height_gNodeB']);
    c = 3*math.pow(10,8);
    typeCoverage = params['type_of_coverage']
    TypeofCoverageLocation = params['coverageLoc'];
    if TypeofCoverageLocation == 'indoor':
        if fc_MHz == 3800:
            PenetrationLoss_indoor = 25.2;
            walls = int(params['number_of_walls'])
            depth = int(params['depth_of_walls'])
            PenetrationLoss_indoor = PenetrationLoss_indoorperdoor*walls
            AttentuationLoss_indoor = depth*4
        else:
            PenetrationLoss_indoorperdoor = 12.8
            walls = int(params['number_of_walls'])
            depth = int(params['depth_of_walls'])
            PenetrationLoss_indoor = PenetrationLoss_indoorperdoor*walls
            AttentuationLoss_indoor = depth*4
    else:
        PenetrationLoss_indoor = 0;
        AttentuationLoss_indoor = 0;

    direction_of_link = params['direction_of_link']
    '''
    UT configuration
    '''
    AntennaGain_Rx = float(params['antennaGain_rx']);
    utnoiseFigure = float(params['utnoise_figure']);
    '''
    QPSk Spectral efficiency: 0.2344 – SINR: -6 dB
    16QAM Spectral efficiency: 2.5703 -SINR 9 dB
    64QAM Spectral efficiency: 5.1152 -SINR 21dB
    256QAM Spectral efficiency: 7.4063 -SINR 35 dB
    '''
    TargetSINR = float(params['targetSINR']);
    CableLoss_Rx = float(params['cable_loss_rx']);
    hUT = float(params['height_UT']);
    
    SlowFadingMargin_dB = float(params['SlowFadingMargin_dB']);
    standarddeviationRural = float(params['standarddeviationRural']);
    confidenceInterval = float(params['confidenceInterval']);
    if fc_MHz==3800:
        isd = 5000;
        BodyLoss_dB = 5;
        FoilageLoss_dB = 11;
        RainMargin_dB = 0;
        if direction_of_link == 'DL':
            InterferenceMargain_dB = 6; '''#calculations for DL'''
        elif direction_of_link == 'UL':
            InterferenceMargain_dB = 2; '''#calculations for UL'''
    else:
        isd = 10000;
        BodyLoss_dB = 2;
        FoilageLoss_dB = 8.5;
        RainMargin_dB = 0;
        InterferenceMargain_dB = 3;
    Receiver_sensitivity_dBm = - utnoiseFigure + ThermalNoise_dB - TargetSINR 
    df1 = []
    '''
    Calaculate the radius at the cell-edge based on the receiver sensitivity
    '''

    max_allowable_prop_pathLoss = Max_Tx_Power - Receiver_sensitivity_dBm + AntennaGain_Tx - CableLoss_Tx + AntennaGain_Rx - CableLoss_Rx - FoilageLoss_dB - BodyLoss_dB - InterferenceMargain_dB -RainMargin_dB - SlowFadingMargin_dB - PenetrationLoss_indoor - AttentuationLoss_indoor
    lambda_m = c/(fc_MHz*math.pow(10,6))
    print(lambda_m)
    
    '''
    invert the free-sapce pathloss 
    '''
    constant = 10*math.log10(lambda_m*lambda_m/(16*math.pi*math.pi))
    if fc_MHz == 700:
        cell_radius_m = math.pow(10, (max_allowable_prop_pathLoss - 5 - 20*math.log10(fc_MHz))/22)
        print(cell_radius_m,'cell_radius_m method 1')
        isd = 2*cell_radius_m
    elif fc_MHz == 3800:
        cell_radius_m = math.pow(10, (max_allowable_prop_pathLoss/1.05+constant)/22)
        print(cell_radius_m,'cell_radius_m methd 2')
        isd = 3*cell_radius_m
        

    output = []
    filename = "cell_radius_Calculator_{}_{}_{}.csv".format(
            params['Bandwidth_MHz'], 
            params['Frequency_MHz'],
            params['FrequencySpacing_KHz'],
        )
    
    output.append({
        'cell_radius_m': cell_radius_m, 
        'Bandwidth_MHz':Bandwidth_MHz,
        'Frequency_MHz':fc_MHz,
        'FrequencySpacing_KHz':FrequencySpacing_KHz,
        'isd':isd,
                   })
    output = pd.DataFrame(output)
    if not os.path.exists('data/Capacity'):
        os.mkdir('data/Capacity')
    my_path = os.path.join('data/Capacity', filename)
    output.to_csv(my_path)
    

a = np.array([1,2])

for a in a:
    capacity(params)
    maximumAllowablePathLoss(params)
    if a == 2:
        params['Frequency_MHz'] = 3800
        params['Bandwidth_MHz'] = 100        
        capacity(params)
        maximumAllowablePathLoss(params)

