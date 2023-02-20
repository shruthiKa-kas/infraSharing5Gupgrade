#!/usr/bin/env python
# coding: utf-8

# In[3]:


import math
import numpy as np
import pandas as pd
import random
import os



params = {
    'demand_gb_month': 50,
    'adoption_rate_perc': 50,
    'cell_radius': 10,
    'mimo_layers': 4,
    'beamforming_mmimo': 'yes',
    'mu_mimo_beams': 10,
    'scaling_factor': 1,
    'bandwidth_Mhz': 10,
    'frequency_Mhz': 700,
    'carrier_spacing_KHz': 15,
    'carrier_aggregation': 1,
    'direction_of_link': 'DL',
    'max_tx_power_dB': 40,
    'number_of_antennas': 64,
    'antenna_Gain_dB': 16,
    'cable_loss_dB': 2,
    'height_gNodeB': 40,
    'type_of_coverage': 'LOS',
    'antenna_gain_rx': 0,
    'generation': '5G',
    'utnoise_figure': 6,
    'target_SINR': - 6,
    'cable_loss_rx': 0,
    'height_UT': 1.5, 
    'coverageType': 'Outdoor',
    'number_of_walls':1,
    'depth_of_wall':1,
    'slow_fading_margin_dB': 7,
    'standarddeviation_rural':6, 
    'confidence_interval': 0.95,
    'environment':'rural',
}


def linkbudgetEsitimation(params):
    '''
    
    This function estimate the link budget between the gNode B and UE at various locations. The model uses the 3GPP NR link budget estimation for downlink (line of sight).
    '''
    
    fc_MHz = float(params['frequency_Mhz'])
    direction_of_link = params['direction_of_link'];
    bandwidth_MHz = float(params['bandwidth_Mhz'])
    frequency_spacing_KHz = float(params['carrier_spacing_KHz'])
    generation = params['generation']
    max_tx_power = float(params['max_tx_power_dB'])
    number_antennas = float(params['number_of_antennas'])
    antenna_gain_tx = float(params['antenna_Gain_dB']);
    cableLoss_tx = float(params['cable_loss_dB']);
    hBS = float(params['height_gNodeB']);
    type_coverage = params['type_of_coverage']
    '''
    UT configuration
    '''
    antenna_gain_rx = float(params['antenna_gain_rx']);
    utnoisefigure = float(params['utnoise_figure']);
    '''
    AdditionalLosses
    '''
    slow_fading_margin_dB = float(params['slow_fading_margin_dB']);
    standarddeviation_rural = float(params['standarddeviation_rural']);
    confidence_interval = float(params['confidence_interval'])
    environment = params['environment']

        
    '''
    QPSk Spectral efficiency: 0.2344 – SINR: -6 dB
    16QAM Spectral efficiency: 2.5703 -SINR 9 dB
    64QAM Spectral efficiency: 5.1152 -SINR 21dB
    56QAM Spectral efficiency: 7.4063 -SINR 35 dB
    '''
    
    target_SINR = float(params['target_SINR']);
    cable_loss_rx = float(params['cable_loss_rx']);
    hUT = float(params['height_UT']);
    type_of_coverage = params['coverageType'];
    
    NbwPRB = float(math.floor(bandwidth_MHz*1000/(frequency_spacing_KHz*12)))-3;
    if frequency_spacing_KHz == 15:
        mu = 0;
        MaxRB = 270;
        if NbwPRB > MaxRB:
            NbwPRB = MaxRB;
    elif frequency_spacing_KHz == 30:
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
   
    Reference_singal_power_dBm = max_tx_power - 10*math.log10(NbwPRB*12)
    Total_transmit_power_dBm = max_tx_power + 10*math.log10(number_antennas)

    TxperPRB = Total_transmit_power_dBm/NbwPRB
    c = 3*math.pow(10,8);

    if type_of_coverage == 'indoor':
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

    '''
    DL losses: Other porpagation losses due to inteference, body loss, foilage, weather, PRBs, sub-carrier power losses and other factors
    '''
    if fc_MHz==3800:
        isd = 5000;
        BodyLoss_dB = 3;
        FoilageLoss_dB = 3;
        RainMargin_dB = 0;
        InterferenceMargain_dB = 6; 
        msc_losses = 20;
    elif fc_MHz== 700:
        isd = 14000;
        BodyLoss_dB = 0;
        FoilageLoss_dB = 0;
        RainMargin_dB = 0;
        InterferenceMargain_dB = 0;
        msc_losses = 35; 

    df1 = []
    for d_UE_Tx in range(100,10000,300):

        output = []
        for _ in range(20):
            '''
            Calculate the pathloss using stochastic modeling, SINR, throughput and spectral efficiency
            for each UE at varying confidence interval.
            '''
            PathLoss_PropagationModel = propgationLosses(hBS,hUT,fc_MHz,c,d_UE_Tx,type_coverage,confidence_interval);
            LinkBudget_SignalAtReceiver = Total_transmit_power_dBm + antenna_gain_tx - cableLoss_tx + antenna_gain_rx - cable_loss_rx -\
            PathLoss_PropagationModel - FoilageLoss_dB - BodyLoss_dB - InterferenceMargain_dB -\
            RainMargin_dB - slow_fading_margin_dB - PenetrationLoss_indoor - AttentuationLoss_indoor - msc_losses
            ThermalNoise_dB = -174 + 10*math.log10(bandwidth_MHz*math.pow(10,6))
            Receiver_sensitivity_dBm = utnoisefigure + ThermalNoise_dB + target_SINR
            SNRdB = LinkBudget_SignalAtReceiver - Receiver_sensitivity_dBm
            SNR = math.pow(10,(SNRdB/10))
            channelThrouput=bandwidth_MHz*math.pow(10,6)*math.log(1+SNR,10)
            if abs(Receiver_sensitivity_dBm) > abs(LinkBudget_SignalAtReceiver):
                y = "pass";
                channelThrouput=bandwidth_MHz*math.pow(10,6)*math.log(1+SNR,10)
            else:
                y = "fail"
                channelThrouput = 0;
            channelThroughout_Mbps = channelThrouput/math.pow(10,6);
            
            '''
            spectral efficiency depends on the PRBS, MIMO and other factors as well
            '''
            if fc_MHz == 3800:
                Multiply = 4;
            if fc_MHz == 700:
                Multiply = 4;
            spectralefficiency = Multiply*channelThrouput/(bandwidth_MHz*math.pow(10,6))
            output.append({
                'iteration': _,
                'environment':environment,
                'bandwidth': bandwidth_MHz,
                'frequecy': fc_MHz,
                'confidence_interval':confidence_interval,
                'distance_m': d_UE_Tx,
                'inter_cell_site_distance': isd,
                'path_loss_db': PathLoss_PropagationModel,
                'LinkBudget_SignalAtReceiver':LinkBudget_SignalAtReceiver,
                'sinr': SNRdB,
                'receiverSensitivty': Receiver_sensitivity_dBm,
                'spectral_efficiency': spectralefficiency,
                'capacity_Mbps': channelThroughout_Mbps,
                'type':type_coverage,
                'generation': generation
            })
       
        output = pd.DataFrame(output)
        df1 = pd.DataFrame(df1)
        if _ == 1:
            df1.drop(df1.index, inplace=True,index=False)
            df1 = output
        else:
            df1 = df1.append(output,ignore_index=True)
        
        filename = "stochasticmodel_{}_{}_{}_{}.csv".format(
            params['frequency_Mhz'], 
            params['bandwidth_Mhz'], 
            params['carrier_spacing_KHz'],
            params['confidence_interval'],
        )
        
        if not os.path.exists('data/Capacity'):
            os.mkdir('data/Capacity')
        my_path = os.path.join('data/Capacity', filename)
        df1.to_csv(my_path, index=False)   
    
    
def propgationLosses(hBS,hUT,fc,c,d_UE_Tx,type_coverage,confidence_interval):
    
    """
    The propagation losses model using rural macro-cell loss estimation RMa model
    
    """
    dBP = 2*math.pi*hBS*hUT*fc*math.pow(10,6)/c;
    d3D = math.sqrt(math.pow(d_UE_Tx,2)+math.pow(hBS-hUT,2))

    W = 20; #m average street width
    h = 5; #m average building height

    if confidence_interval == 0.95:
        z = 1.959;
    elif confidence_interval == 0.9:
        z = 1.644;
    elif confidence_interval == 0.8:
        z = 1.28;
    elif confidence_interval == 0.05:
        z = 0.06;
    if type_coverage == "LOS":
        standarddeviation_rural = 5.6;
        mu = 0;
        if d_UE_Tx < dBP:
            PLRMaLOSresults = pathlossLOScal(d3D,fc,h) + mu + z*standarddeviation_rural
            PLRMaLOSresults = PLRMaLOSresults*random.uniform(confidence_interval, 1)
        elif d_UE_Tx < 10000:
            PLRMaLOSresults = pathlossLOScal(dBP,fc,h) + 40*math.log10(d3D/dBP) + mu + z*standarddeviation_rural
            PLRMaLOSresults = PLRMaLOSresults*random.uniform(confidence_interval, 1)
        return PLRMaLOSresults
    
def pathlossLOScal(d3D,fc,h):
    """
    Line of sight (LOS) path loss estimation as per 3GPP RMa model, with standard deviation 6 and mean 0
    
    """
    PLRMaLOS = 20*math.log10(40*math.pi*d3D*fc/3000) + min(0.03*math.pow(h,1.72), 10)*math.log10(d3D) - min(0.044*math.pow(h,1.72), 14.77) + 0.002*math.log10(h)*d3D
    return PLRMaLOS



a = np.array([1,2])
for a in a:
    linkbudgetEsitimation(params)
    if a == 2:
        params['frequency_Mhz'] = 3800
        params['bandwidth_Mhz'] = 100 
        params['carrier_spacing_KHz'] = 30
        linkbudgetEsitimation(params)

