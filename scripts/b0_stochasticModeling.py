#!/usr/bin/env python
# coding: utf-8

# In[3]:


import math
import numpy as np
import pandas as pd
import random
import os


def linkbudgetEsitimation(params):
    fc_MHz = float(params['frequency_Mhz'])
    DirectionofLink = "UL";
    Bandwidth_MHz = float(params['bandwidth_Mhz'])
    FrequencySpacing_KHz = float(params['carrier_spacing_KHz'])
    generation = params['generation']
     #Transmit power per PRB, dBm=(Total output power RRH/RRU/AAU) /(Max number of PRB for Bandwidth)
    Max_Tx_Power = float(params['Max_Tx_Power_dB'])
    No_Antennas = float(params['number_of_antennas'])
    AntennaGain_Tx = float(params['antenna_Gain_dB']);
    CableLoss_Tx = float(params['cable_loss_dB']);
    hBS = float(params['height_gNodeB']);
    typeCoverage = params['type_of_coverage']
    #UT configuration
    AntennaGain_Rx = float(params['antennaGain_rx']);
    utnoiseFigure = float(params['utnoise_figure']);
        #AdditionalLosses
    SlowFadingMargin_dB = float(params['SlowFadingMargin_dB']);
    standarddeviationRural = float(params['standarddeviationRural']);
    confidenceInterval = float(params['confidence_interval'])
    environment = params['environment']
    # 0.95;
        
#     QPSk Spectral efficiency: 0.2344 – SINR: -6 dB
# 16QAM Spectral efficiency: 2.5703 -SINR 9 dB
# 64QAM Spectral efficiency: 5.1152 -SINR 21dB
# 256QAM Spectral efficiency: 7.4063 -SINR 35 dB
    TargetSINR = float(params['targetSINR']);
    CableLoss_Rx = float(params['cable_loss_rx']);
    hUT = float(params['height_UT']);
    TypeofCoverage = params['coverageType'];
    
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
    #gNodeB configuration
   
    Reference_singal_power_dBm = Max_Tx_Power - 10*math.log10(NbwPRB*12)
    Total_transmit_power_dBm = Max_Tx_Power + 10*math.log10(No_Antennas)
    # print(Reference_singal_power_dBm, 'Reference_singal_power_dBm')
    # print(Total_transmit_power_dBm, 'Total_transmit_power_dBm')
    
    #TransmitPower_TxBW = int(input("Enter total RRH power (in dBm)"))
    TxperPRB = Total_transmit_power_dBm/NbwPRB
    c = 3*math.pow(10,8);
    


    if TypeofCoverage == 'indoor':
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

    
    if fc_MHz==3800:
        isd = 5000;
        BodyLoss_dB = 3;
        FoilageLoss_dB = 3;
        RainMargin_dB = 0;
        InterferenceMargain_dB = 6; #All calculations for DL
        msc_losses = 20; #due to PRBs, sub-carrier power losses and other factors
    elif fc_MHz== 700:
        isd = 14000;
        BodyLoss_dB = 0;
        FoilageLoss_dB = 0;
        RainMargin_dB = 0;
        InterferenceMargain_dB = 0;
        msc_losses = 35; #due to PRBs, sub-carrier power losses and other factors

        
#     def generate_site_radii(min, max, increment):
#         for n in range(min, max, increment):
#             yield n

#     INCREMENT_MA = (400, 40400, 1000)

#     SITE_RADII = {
#         'macro': {
#            generate_site_radii(INCREMENT_MA[0],INCREMENT_MA[1],INCREMENT_MA[2])
#             },
#         }
    # --- before loop ---

    # <-- list for all results
    
    df1 = []
    for d_UE_Tx in range(100,10000,300):
        #d_UE_Tx = int(input('Enter distance between Tx and UE (in m)'));

        output = []
        for _ in range(20):
            PathLoss_PropagationModel = propgationLosses(hBS,hUT,fc_MHz,c,d_UE_Tx,typeCoverage,confidenceInterval);
            #print(PathLoss_PropagationModel)
            #PathLoss_PropagationModelstandardDevidation = PathLoss_PropagationModel - 1.96*standarddeviationRural/math.sqrt(20)+20;
            #print(PathLoss_PropagationModelstandardDevidation)
             #PathLoss_PropagationModelstandardDevidation
            LinkBudget_SignalAtReceiver = Total_transmit_power_dBm + AntennaGain_Tx - CableLoss_Tx + AntennaGain_Rx - CableLoss_Rx -                                         PathLoss_PropagationModel - FoilageLoss_dB - BodyLoss_dB - InterferenceMargain_dB -                                         RainMargin_dB - SlowFadingMargin_dB - PenetrationLoss_indoor - AttentuationLoss_indoor - msc_losses
            #print(LinkBudget_SignalAtReceiver)
            #Receiver sensitivity (dBm) = Noise figure (dB) + Thermal noise (dBm) + SINR (dB)
            #Thermal noise =-174+10log("bandwidth" Hz)
            ThermalNoise_dB = -174 + 10*math.log10(Bandwidth_MHz*math.pow(10,6))
            # 10*math.log10(1.38*294*Bandwidth_MHz*math.pow(10,6)*math.pow(10,-23))
            #-174 + 10*math.log10(Bandwidth*math.pow(10,6))
            #print(ThermalNoise)
            Receiver_sensitivity_dBm = utnoiseFigure + ThermalNoise_dB + TargetSINR
            #print(ReceiverSensitivity)
            SNRdB = LinkBudget_SignalAtReceiver - Receiver_sensitivity_dBm
            #print(SNRdB)
            SNR = math.pow(10,(SNRdB/10))
            channelThrouput=Bandwidth_MHz*math.pow(10,6)*math.log(1+SNR,10)
            #Receiver Sensitivity
            # Receiver sensitivity (dBm) = Noise figure (dB) + Thermal noise (dBm) + SINR (dB)
            #channelThrouput 
            if abs(Receiver_sensitivity_dBm) > abs(LinkBudget_SignalAtReceiver):
                y = "pass";
                channelThrouput=Bandwidth_MHz*math.pow(10,6)*math.log(1+SNR,10)
                #print("channelThrouput", channelThrouput)
                #print("spectralefficiency", spectralefficiency)
                #spectrum = fc_MHz*math.pow(10,6);
            else:
                y = "fail"
                channelThrouput = 0;
            channelThroughout_Mbps = channelThrouput/math.pow(10,6);
            
            #spectral efficiency depends on the PRBS as well
            if fc_MHz == 3800:
                Multiply = 4; #MIMO and other factors
            if fc_MHz == 700:
                Multiply = 4; #MIMO and other factors
            spectralefficiency = Multiply*channelThrouput/(Bandwidth_MHz*math.pow(10,6))
            output.append({
                'iteration': _,
                'environment':environment,
                'bandwidth': Bandwidth_MHz,
                'frequecy': fc_MHz,
                'confidence_interval':confidenceInterval,
                'distance_m': d_UE_Tx,
                'inter_cell_site_distance': isd,
                'path_loss_db': PathLoss_PropagationModel,
                #PathLoss_PropagationModelstandardDevidation,
                'LinkBudget_SignalAtReceiver':LinkBudget_SignalAtReceiver,
                'sinr': SNRdB,
                'receiverSensitivty': Receiver_sensitivity_dBm,
                # 'radio_channel_status': y,
                'spectral_efficiency': spectralefficiency,
                'capacity_Mbps': channelThroughout_Mbps,
                'type':typeCoverage,
                'generation': generation
            })
       
        # output = pd.DataFrame(output)
        output = pd.DataFrame(output)
        output.to_csv('ThroughputCapacityoutput.csv')
        #print(PathLoss_PropagationModel)
        #=[@[Throughput MBps]]-[@Zvalue]*[@StandardDeviation]/SQRT([@NumberofObservations]) 
        df1 = pd.DataFrame(df1)
        if _ == 1:
            df1.drop(df1.index, inplace=True,index=False)
            df1 = output
        else:
            df1 = df1.append(output,ignore_index=True)
        
        filename = "StochasticModel_{}_{}_{}_{}.csv".format(
            params['frequency_Mhz'], 
            params['bandwidth_Mhz'], 
            params['carrier_spacing_KHz'],
            params['confidence_interval'],
        )
        
        if not os.path.exists('results/Capacity'):
            os.mkdir('results/Capacity')
        my_path = os.path.join('results/Capacity', filename)
        df1.to_csv(filename, index=False)   
    
    



#model propagation Losses
def propgationLosses(hBS,hUT,fc,c,d_UE_Tx,typeCoverage,confidenceInterval):
    
    """
    Function explanation...
    
    """
    dBP = 2*math.pi*hBS*hUT*fc*math.pow(10,6)/c;
    d3D = math.sqrt(math.pow(d_UE_Tx,2)+math.pow(hBS-hUT,2))
    #print(d3D/dBP)
    W = 20; #m average street width
    h = 5; #m average building height
    #x =  random.uniform(math.pow(math.e,-1*(d_UE_Tx-10)/1000),1)
    # x = random.uniform(0.95,1)
    # print(x)
    #random.uniform(0.95, 1)
    if confidenceInterval == 0.95:
        z = 1.959;
    elif confidenceInterval == 0.9:
        z = 1.644;
    elif confidenceInterval == 0.8:
        z = 1.28;
    elif confidenceInterval == 0.05:
        z = 0.06;
    if typeCoverage == "LOS":
        standarddeviationRural = 5.6;
        mu = 0;
        if d_UE_Tx < dBP:
            PLRMaLOSresults = pathlossLOScal(d3D,fc,h) + mu + z*standarddeviationRural
            PLRMaLOSresults = PLRMaLOSresults*random.uniform(confidenceInterval, 1)
        elif d_UE_Tx < 10000:
            PLRMaLOSresults = pathlossLOScal(dBP,fc,h) + 40*math.log10(d3D/dBP) + mu + z*standarddeviationRural
            PLRMaLOSresults = PLRMaLOSresults*random.uniform(confidenceInterval, 1)
        return PLRMaLOSresults
    
def pathlossLOScal(d3D,fc,h):
    """
    Function explanation...
    
    """
    PLRMaLOS = 20*math.log10(40*math.pi*d3D*fc/3000) + min(0.03*math.pow(h,1.72), 10)*math.log10(d3D) - min(0.044*math.pow(h,1.72), 14.77) + 0.002*math.log10(h)*d3D
    return PLRMaLOS



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
    'direction_of_link': 'UL',
    'Max_Tx_Power_dB': 40,
    'number_of_antennas': 64,
    'antenna_Gain_dB': 16,
    'cable_loss_dB': 2,
    'height_gNodeB': 40,
    'type_of_coverage': 'LOS',
    'antennaGain_rx': 0,
    'generation': '5G',
    'utnoise_figure': 6,
    'targetSINR': - 6,
    'cable_loss_rx': 0,
    'height_UT': 1.5, 
    'coverageType': 'Outdoor',
    'number_of_walls':1,
    'depth_of_wall':1,
    'SlowFadingMargin_dB': 7,
    'standarddeviationRural':6, 
    'confidence_interval': 0.95,
    'environment':'rural',
}




a = np.array([1,2])
# b = np.array([0.05,0.8,0.90,0.95])
# for b in b:
#     params['confidence_interval'] = b
#     print(b)
for a in a:
    linkbudgetEsitimation(params)
    if a == 2:
        params['frequency_Mhz'] = 3800
        params['bandwidth_Mhz'] = 100 
        params['carrier_spacing_KHz'] = 30
        linkbudgetEsitimation(params)

