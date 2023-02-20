#!/usr/bin/python
# -*- coding: utf-8 -*-

# In[31]:

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
import csv

'''
This module performs the cost estimation of different components and assesses
the total cost of ownership for different infrastructure strategies.
'''

params = {
    'cost_RAN_small_USD': 500,
    'cost_spectrum_700_USD': 0.28,
    'cost_spectrum_3800_USD': 0.03,
    'Core_cost_percentage': 0.1,
    'OPEX_rental': 0.1,
    'backhaul_MC': 10000,
    'backhaul_SC_m': 5,
    'tower': 1000,
    'SiteRental_rural_macro': 1000,
    'siteRental_rural_small': 200,
    'carrier_aggregation': 1,
    'power_supply': 250,
    'Control_units': 2000,
    'IO_fronthaul': 1500,
    'Remote_radio_units': 3500,
    'processing': 1500,
    'population': 18000,
    'debt': 0.05,
    'opex_small': 800,
    'CAPEX_rateofChange': -0.03,
    'OPEX_rateofChange': 0.05,
    'Badloans_rateofChange': 0.02,
    'Customer_growth_rate': 0.04,
    'bandwidth_700Mhz': 10,
    'bandwidth_3800MHz': 100,
    'run_only_once': 0,
    'existing_site_density_per_km2': 0.02,
    'coverage_area_km2': 500,
    'population_density': 36,
    'cell_radius_MC': 6,
    'cell_radius_SC': 3.5,
    'contention': 10,
    'backhaul_capacity_Gbps': 5,
    'demand_gb_month': 50,
    'adoption_rate_perc': 0.5,
    'area_covered': 500,
    }


def costEstimate(params):
    """
    Estimate the cost of different type of infrastructure sharing model
    """

    population_density = int(params['population_density'])
    filename = 'Overall_cellrequired_macro_small.csv'
    my_path = os.path.join('data/Capacity', filename)
    df = pd.read_csv(my_path)
    arr = df.to_numpy()
    index = np.where(arr == population_density)
    [iteration, population_density, Number_of_MC_upgrade,
     Number_of_SC_deployed, overall_towers] = arr[1, :]
    cost_RAN_small_USD = float(params['cost_RAN_small_USD'])
    cost_spectrum_700_USD = float(params['cost_spectrum_700_USD'])
    cost_spectrum_3800_USD = float(params['cost_spectrum_3800_USD'])
    existing_towers_SC = int(Number_of_SC_deployed)
    existing_towers_MC = int(Number_of_MC_upgrade)
    core_cost_percentage = float(params['Core_cost_percentage'])
    OPEX_rental = params['OPEX_rental']
    backhaul_MC = params['backhaul_MC']
    backhaul_SC_m = float(params['backhaul_SC_m'])
    tower = float(params['tower'])
    siteRental_rural_macro = float(params['SiteRental_rural_macro'])
    siteRental_rural_small = float(params['siteRental_rural_small'])
    carrier_aggregation = float(params['carrier_aggregation'])
    power_supply = float(params['power_supply'])
    control_units = params['Control_units']
    iO_fronthaul = float(params['IO_fronthaul'])
    remote_radio_units = float(params['Remote_radio_units'])
    processing = float(params['processing'])
    population = float(params['population'])
    debt = float(params['debt'])
    opex_small = float(params['opex_small'])

    bandwidth_700Mhz = float(params['bandwidth_700Mhz'])
    bandwidth_3800MHz = float(params['bandwidth_3800MHz'])
    CAPEX_small = cost_RAN_small_USD
    siteRental_rural_small = siteRental_rural_small
    siteRental_rural_macro = siteRental_rural_macro
    CAPEX_macro = carrier_aggregation + control_units + iO_fronthaul \
        + remote_radio_units + processing
    year = np.array([
        2023,
        2024,
        2025,
        2026,
        2027,
        2028,
        2029,
        2030,
        2031,
        2032,
        ])
    CAPEX_rateofChange = float(params['CAPEX_rateofChange'])
    OPEX_rateofchange = float(params['OPEX_rateofChange'])
    Badloans_rateofChange = float(params['Badloans_rateofChange'])
    CAPEX_rateofChange = np.power(1 + CAPEX_rateofChange, year - 2023)
    OPEX_rateofchange = np.power(1 + OPEX_rateofchange, year - 2023)
    Badloans_rateofChange = np.power(1 + Badloans_rateofChange, year
            - 2023)

    OPEX_small = (opex_small + power_supply / 4) * 10
    OPEX_macro = (OPEX_rental * CAPEX_macro + power_supply) * 10

    Core = core_cost_percentage * (existing_towers_SC
                                   * cost_RAN_small_USD
                                   + existing_towers_MC
                                   * (carrier_aggregation
                                   + control_units + iO_fronthaul
                                   + remote_radio_units + processing))

    Type = np.array(['NS', 'PS', 'AS', 'NHN'])

    def eachCasecost(type):
        '''
        For 4 operators scenario
        t : number of towers upgrade
        b : number of backhaul upgrade
        s : number of spectrum upgrade
        r : number of RAN upgrade
        c : number of Core upgrade
        '''

        if type == 'NS':
            
            t = 4
            b = 4
            s = 4
            r = 4
            c = 4
            strategy = np.array([
                'Solo',
                'Solo',
                'Solo',
                'Solo',
                'Solo',
                'Solo',
                'Solo',
                'Solo',
                'Solo',
                'Solo',
                ])
        elif type == 'PS':
            t = 1
            b = 1
            s = 4
            r = 4
            c = 4
            strategy = np.array([
                'Passive',
                'Passive',
                'Passive',
                'Passive',
                'Passive',
                'Passive',
                'Passive',
                'Passive',
                'Passive',
                'Passive',
                ])
        elif type == 'AS':
            t = 1
            b = 1
            s = 2
            r = 2
            c = 4
            strategy = np.array([
                'Active',
                'Active',
                'Active',
                'Active',
                'Active',
                'Active',
                'Active',
                'Active',
                'Active',
                'Active',
                ])
        elif type == 'NHN':
            t = 1
            b = 1
            s = 1
            r = 1
            c = 1
            strategy = np.array([
                'NHN5G',
                'NHN5G',
                'NHN5G',
                'NHN5G',
                'NHN5G',
                'NHN5G',
                'NHN5G',
                'NHN5G',
                'NHN5G',
                'NHN5G',
                ])

        CAPEX = (CAPEX_small * existing_towers_SC * r
                 + siteRental_rural_small * t + bandwidth_3800MHz
                 * cost_spectrum_3800_USD * population * s
                 + backhaul_SC_m * 1000 * b + CAPEX_macro
                 * existing_towers_MC * r + siteRental_rural_macro * t
                 + Core * c + bandwidth_700Mhz * cost_spectrum_700_USD
                 * population * s + backhaul_MC * b) / 10 \
            * CAPEX_rateofChange
        OPEX = (OPEX_small * existing_towers_SC * r + OPEX_macro
                * existing_towers_MC * r) / 10 * OPEX_rateofchange
        TCO = CAPEX + OPEX

        # print(TCO_NS, 'TCO_NS')

        Badloans = TCO * Badloans_rateofChange
        TCO_plus_badloans = TCO + Badloans

        arr = np.stack((
            strategy,
            year,
            np.round(CAPEX),
            np.round(OPEX),
            np.round(Badloans),
            np.round(TCO_plus_badloans),
            ), axis=1)
        return arr

    for type in Type:
        '''
        Estimate cost for each type of sharing for the estimated number of macro
        upgraded and small cell deployment requied -
        "Solo", 
        "Passive", 
        "Active", 
        "NHN5G"   
        ''' 
        a = eachCasecost(type)
        filename = 'cost_{}_{}_{}.csv'.format(existing_towers_MC,
                existing_towers_SC, type)
        output = pd.DataFrame(a, columns=[
            'Scenario',
            'Year',
            'CAPEX',
            'OPEX',
            'Debt',
            'TCO',
            ])
        if not os.path.exists('data/Cost'):
            os.mkdir('data/Cost')
        my_path = os.path.join('data/Cost', filename)
        output.to_csv(my_path)


costEstimate(params)
