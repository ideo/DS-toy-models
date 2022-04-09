import pandas as pd
from src.simulation import Simulation
from src.guacamoles import Guacamoles


def param_space_scan_all_guacs_for_all():
        
    scenarios = ['A Lot of Contenders', 'One Clear Winner', 'A Close Call']
    num_guacs = 20
    num_guacs_per_voter = 20
    num_townspeople = 200
    stds = [2,4,6]
    pct_like = [0,25,50]
    pct_dislike = [0,10,20,30,40,50]
    total_number_simulations = 100

    for scenario in scenarios:

        #create guac sample based on selection
        guacs = Guacamoles(num_guacs, scenario)
        guac_df = guacs.df

        scenario = '-'.join(scenario.lower().split(' '))

        rows = []
        for metric in ['sum']:
            for std in stds:
                for plike in pct_like:
                    for pdislike in pct_dislike:

                        for tns in range(total_number_simulations):
                            
                            sim = Simulation(guac_df, num_townspeople, std, 
                                        pct_ppl_really_like=plike, 
                                        pct_ppl_really_dislike=pdislike, 
                                        num_guacs_per_voter=num_guacs_per_voter, 
                                        fullness_factor=True)
                            
                            sim.simulate(winner_metric=metric)

                            #collect data for dataframe
                            row = {}
                            row['metric'] = metric
                            row['scenario'] = scenario
                            row['num_townspeople'] = num_townspeople
                            row['num_guacs_per_voter'] = num_guacs_per_voter
                            row['std'] = std
                            row['pct_ppl_like'] = plike
                            row['pct_ppl_dislike'] = pdislike
                            row['loop_step'] = tns
                            

                            #record the outcome of this step:
                            if sim.winner == sim.true_winner:
                                row[f"true_winner_recovered"] = 'true'
                            else:
                                row[f"true_winner_recovered"] = 'false'

                            print(f"{tns} - cmetric = {metric}, scenario = {row['scenario']}, std = {std}, pct_ppl_like = {plike}, pct_ppl_dislike = {pdislike}, result = ", row["true_winner_recovered"])

                            #incrementing multiple winners if that's the case
                            if len(sim.winners) > 1: 
                                row[f"multiple_winners"] = 'true'
                                print('multiple winners!')
                            else:
                                row[f"multiple_winners"] = 'false'

                            rows.append(row)

        #saving the data in multiple steps
        my_filename = f"data/param_space_scan_totalSim{total_number_simulations}_{scenario}_{metric}.csv"
        df = pd.DataFrame(rows)
        df.to_csv(my_filename)

def param_space_scan():
        
    #all guacs to all config
    scenarios = ['A Lot of Contenders', 'One Clear Winner', 'A Close Call']
    scenarios = ['A Lot of Contenders']
    metrics = ['sum']    
    num_guacs = 20
    num_guacs_per_voter_list = [20]
    num_townspeople = 200
    stds = [2,4,6]
    pct_like = [0,25,50]
    pct_dislike = [0,10,20,30,40,50]
    total_number_simulations = 5

    # #guacs subset
    # scenarios = ['A Lot of Contenders']
    # metrics = ['condorcet']
    # num_guacs = 20
    # num_guacs_per_voter_list = list(range(20,1,-1))
    # num_townspeople = 300
    # stds = [2,4,6]
    # pct_like = [33]
    # pct_dislike = [33]
    # total_number_simulations = 200

    for scenario in scenarios:

        #create guac sample based on selection
        guacs = Guacamoles(num_guacs, scenario)
        guac_df = guacs.df

        scenario = '-'.join(scenario.lower().split(' '))

        rows = []
        for metric in metrics:
            for std in stds:
                for plike in pct_like:
                    for pdislike in pct_dislike:

                        for tns in range(total_number_simulations):

                            #collect data for dataframe
                            row = {}
                            row['metric'] = metric
                            row['scenario'] = scenario
                            row['num_townspeople'] = num_townspeople
                            row['std'] = std
                            row['pct_ppl_like'] = plike
                            row['pct_ppl_dislike'] = pdislike
                            row['loop_step'] = tns

                            fraction_multiple_winners = 0
                            for ngpv in num_guacs_per_voter_list:

                            
                                sim = Simulation(guac_df, num_townspeople, std, 
                                            pct_ppl_really_like=plike, 
                                            pct_ppl_really_dislike=pdislike, 
                                            num_guacs_per_voter=ngpv, 
                                            fullness_factor=True)
                                
                                sim.simulate(winner_metric=metric)

                                
                                #If giving everyone all guacs
                                if len(num_guacs_per_voter_list) == 1 and num_guacs_per_voter_list[0] == num_guacs:
    
                                    row['num_guacs_per_voter'] = ngpv
                                    
                                    #record the outcome of this step:
                                    if sim.winner == sim.true_winner:
                                        row[f"true_winner_recovered"] = 'true'
                                    else:
                                        row[f"true_winner_recovered"] = 'false'


                                    #incrementing multiple winners if that's the case
                                    if len(sim.winners) > 1: 
                                        row[f"multiple_winners"] = 'true'
                                        print('multiple winners!')
                                    else:
                                        row[f"multiple_winners"] = 'false'

                                    print(f"{tns} - cmetric = {metric}, scenario = {row['scenario']}, std = {std}, pct_ppl_like = {plike}, pct_ppl_dislike = {pdislike}, result = ", row["true_winner_recovered"])
                                else:
                                    #record the outcome of this step:
                                    #if not all guacs have been assigned, then the configuration is not fair
                                    if len(sim.results_df[sim.results_df['mean'].isnull()]) > 0:
                                        # print('Not all quacs assigned!')
                                        row[f"guac_{ngpv}"] = 'not_all_assigned'
                                        row[f"guac_{ngpv}"] = 'not_all_assigned'
                                    else:
                                        if sim.winner == sim.true_winner:
                                            row[f"guac_{ngpv}"] = 'true'
                                        else:
                                            row[f"guac_{ngpv}"] = 'false'

                                        if len(sim.winners) > 1:
                                            fraction_multiple_winners += 1

                                    print(f"{tns} - metric = {metric}, scenario = {row['scenario']}, std = {std}, pct_ppl_like = {plike}, pct_ppl_dislike = {pdislike}, ngpv = {ngpv}, result = ", row[f"guac_{ngpv}"])


                            if len(num_guacs_per_voter_list) > 1:
                                row[f"fraction_multiple_winners"] = fraction_multiple_winners/total_number_simulations

                            rows.append(row)

        #saving the data in multiple steps
        if len(num_guacs_per_voter_list) == 1 and num_guacs_per_voter_list[0] == 20:
            my_filename = f"data/param_space_scan_totalSim{total_number_simulations}_{scenario}_{metric}.csv"
        else:
            my_filename = f"data/param_space_scan_guacs_subset_totalSim{total_number_simulations}_townpeople{num_townspeople}_{scenario}_{metric}.csv"
            
        df = pd.DataFrame(rows)
        df.to_csv(my_filename)
    

if __name__ == "__main__":
    param_space_scan()
    print('DONE')
