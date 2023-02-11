import math
import numpy as np
import random
import pandas as pd
import os

params = {
    'existing_site_density_per_km2': 0.02,
    'coverage_area_km2': 500,
    'population_density':36,
    'cell_radius_MC':6,
    'cell_radius_SC':3.5,
    'contention':10,
    'backhaul_capacity_Gbps': 5,
}



def TowerRequired(params):
    existing_site_density_per_km2 = float(params['existing_site_density_per_km2'])
    coverage_area_km2 = float(params['coverage_area_km2'])
    population_density = float(params['population_density'])
    cell_radius_MC = float(params['cell_radius_MC'])
    cell_radius_SC = float(params['cell_radius_SC'])
    contention = float(params['contention'])
    backhaul_capacity_Gbps = float(params['backhaul_capacity_Gbps'])
    Total_existing_sites = coverage_area_km2*existing_site_density_per_km2
    print(Total_existing_sites, 'Total_existing_sites')
    NumberOfPeople = population_density*coverage_area_km2;
    upgrade_subscribers = 0.3*0.5*NumberOfPeople;
    Additional_5G_subscribers = 0.2*NumberOfPeople;
    total_subscribers_5G = upgrade_subscribers + Additional_5G_subscribers
    overall_subscribers = total_subscribers_5G + total_subscribers_5G
    
    def congestionEstimation(Number_of_MC_upgrade, Number_of_SC_deployed):
        #condition to check if upgrade is sufficient
        Total_existing_subscribers = 0.5*NumberOfPeople;
        number_of_users_supported_30Mbps = Number_of_MC_upgrade*1000*backhaul_capacity_Gbps/30
        number_of_users_supported_10Mbps = Number_of_MC_upgrade*1000*backhaul_capacity_Gbps/10
        # print(round(number_of_users_supported_30Mbps,0),'number_of_users_supported_30Mbps active')
        # print(round(number_of_users_supported_10Mbps,0),'number_of_users_supported_10Mbps active')
        with_contention_users_30Mbps = contention*number_of_users_supported_30Mbps;
        with_contention_users_10Mbps = contention*number_of_users_supported_10Mbps;
        # print(round(with_contention_users_30Mbps,0),'with_contention_users_30Mbps')
        # print(round(with_contention_users_10Mbps,0), 'with_contention_users_10Mbps')

        number_of_users_supported_SC_30Mbps = Number_of_SC_deployed*1000*backhaul_capacity_Gbps/300
        number_of_users_supported_SC_10Mbps = Number_of_SC_deployed*1000*backhaul_capacity_Gbps/100
        # print(round(number_of_users_supported_300Mbps,0),'number_of_users_supported_300Mbps active')
        # print(round(number_of_users_supported_100Mbps,0),'number_of_users_supported_100Mbps active')
        with_contention_users_SC_30Mbps = contention*number_of_users_supported_SC_30Mbps;
        with_contention_users_SC_10Mbps = contention*number_of_users_supported_SC_10Mbps;
        return with_contention_users_10Mbps, with_contention_users_30Mbps,with_contention_users_SC_30Mbps,with_contention_users_SC_10Mbps       

    def upgradetowers():            
        Area_coverage_MC = math.pi*math.pow(cell_radius_MC,2)
        Area_coverage_SC = math.pi*math.pow(cell_radius_SC,2)
        print(round(Area_coverage_MC,0), 'Area_coverage_MC')
        print(round(Area_coverage_SC,0), 'Area_coverage_SC')
        Number_of_MC_upgrade = coverage_area_km2/Area_coverage_MC
        Number_of_SC_deployed = coverage_area_km2/Area_coverage_SC
        print(round(Number_of_MC_upgrade,0),'Number_of_MC_upgrade')
        print(round(Number_of_SC_deployed,0),'Number_of_SC_deployed')
        return Number_of_MC_upgrade, Number_of_SC_deployed

    def upgradeconditions(Number_of_MC_upgrade,Number_of_SC_deployed):
        #estimate whether the upgrade is sufficient or not
        # y = 6;
        [with_contention_users_10Mbps, with_contention_users_30Mbps, with_contention_users_SC_30Mbps,with_contention_users_SC_10Mbps] = congestionEstimation(Number_of_MC_upgrade,Number_of_SC_deployed)
        if Number_of_MC_upgrade < Total_existing_sites:
            # print('loop')
            # print(round(with_contention_users_300Mbps,0),'with_contention_users_300Mbps')
            # print(round(with_contention_users_100Mbps,0),'with_contention_users_100Mbps')
            #Condition to check if more towers are being upgrade or not
            # print('reached here')
            # if Number_of_MC_upgrade > Total_existing_sites:
            #     print('consider greenfield deployment')
            # else:
            if with_contention_users_10Mbps > overall_subscribers:
                print('Universal coverage obligation is satisfied.')
                # return Number_of_MC_upgrade,Number_of_SC_deployed
                if with_contention_users_30Mbps - total_subscribers_5G > 2000:
                    print('This network can support a minimum of 30 Mbps per user and can support an additional',round(with_contention_users_30Mbps - total_subscribers_5G,0), 'active subscribers. Consider replanning the network upgrade requirements the sites for upgrade');
                    Number_of_MC_upgrade = Number_of_MC_upgrade - 1;
                    Number_of_SC_deployed = Number_of_SC_deployed - 1;
                    print('Try with', round(Number_of_MC_upgrade,0),round(Number_of_SC_deployed,0), 'Number_of_MC_upgrade,Number_of_SC_deployed')
                    # x = 1;
                    # upgradeconditions(Number_of_MC_upgrade,Number_of_SC_deployed)
                    return Number_of_MC_upgrade,Number_of_SC_deployed
                elif with_contention_users_30Mbps < total_subscribers_5G:
                    print('add towers or increase backhaul for macro speeds');
                    Number_of_MC_upgrade = Number_of_MC_upgrade + 1;
                    Number_of_SC_deployed = Number_of_SC_deployed + 1;
                    # print('Increase the number of towers')
                    # x = 1;
                    if with_contention_users_SC_30Mbps > total_subscribers_5G-with_contention_users_30Mbps:
                        print('However, small cells can support it')
                    else:
                        print('Increase small cells as well')
                    return Number_of_MC_upgrade,Number_of_SC_deployed
                else:
                    print('sufficient upgrade for 30Mbps data rate');
                    # y = 'sufficient upgrade';
                    if with_contention_users_SC_30Mbps > total_subscribers_5G-with_contention_users_30Mbps:
                        print('Small cells can support it as well')
                    else:
                        print('Increase small cells as well')
                    print('Upgrade with', round(Number_of_MC_upgrade,0), 'Number_of_MC_upgrade and deploy', round(Number_of_SC_deployed,0),'Number_of_SC_deployed')
                    # x = 0;
                    
                    return Number_of_MC_upgrade,Number_of_SC_deployed
                    
                    # upgradeconditions(Number_of_MC_upgrade,Number_of_SC_deployed)
            else:
                print('Network is congested at current parameters')
                return Number_of_MC_upgrade,Number_of_SC_deployed

    [Number_of_MC_upgrade, Number_of_SC_deployed] = upgradetowers();
    [Number_of_MC_upgrade, Number_of_SC_deployed] = upgradeconditions(Number_of_MC_upgrade,Number_of_SC_deployed)
    output = []
    filename = "Upgrade.csv"
    output.append({
        'Number_of_MC_upgrade': Number_of_MC_upgrade,
        'Number_of_SC_deployed': Number_of_SC_deployed,
        'population_density':population_density,
        'coverage_area_km2':coverage_area_km2,
    })

    output = pd.DataFrame(output)
    if not os.path.exists('results/UpgradeRequirements'):
        os.mkdir('results/UpgradeRequirements')
    my_path = os.path.join('results/UpgradeRequirements', filename)
    output.to_csv(my_path)
    return Number_of_MC_upgrade,Number_of_SC_deployed
[Number_of_MC_upgrade,Number_of_SC_deployed] = TowerRequired(params)