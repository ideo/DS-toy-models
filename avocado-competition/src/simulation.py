import random
import os
import sys
import numpy as np
import pandas as pd

this_file_path = os.path.dirname(__file__)
sys.path.append(this_file_path)

import utils
from .townspeople import Townsperson
from .condorcetcounting import Condorcetcounting
from random import sample

#TODO Fix parameter space scan to test for not all guacs being assigmed

class Simulation:
    def __init__(
        self, 
        guac_df,
        num_townspeople, 
        st_dev, 
        pct_ppl_really_like = 0.0, 
        pct_ppl_really_dislike = 0.0, 
        num_guacs_per_voter = 20, 
        fullness_factor = False
        ):

        #assigned guacs per person
        self.num_guacs_per_voter = num_guacs_per_voter

        #dataframe with guacs and objective voting
        self.guac_df = guac_df

        #number of townspeople voting
        self.num_townspeople = num_townspeople

        #fraction of townpeople that tend to upvote
        self.frac_upvoting = pct_ppl_really_like/100.0

        #fraction of townpeople that tend to downvote
        self.frac_downvoting = pct_ppl_really_dislike/100.0

        #standard deviation for the toe
        self.st_dev = st_dev

        #count of people that tend to upvote, downvote, and be reasonable
        self.num_ppl_really_like, self.num_ppl_really_dislike, self.num_ppl_neutral=self.get_personas_counts()
        
        #dictionary with each persona mean offset and standard devitaion
        self.personas = self.create_personas()

        #dataframe that contains all scores for all guacs
        self.results_df = pd.DataFrame()

        #columns with the scores
        self.scores_cols = []

        #winners
        self.winner = None
        self.winners = []

        self.true_winner = self.guac_df.sort_values(by=['objective_score'], ascending=False).iloc[0]['id']


        #accounting for fullness and decreasing the score accordingly
        self.fullness_factor = fullness_factor

    def get_personas_counts(self):
        """This function creates the counts for the different personas.

        Returns:
           tuple of integers with the count for each persona
        """

        #number of people that tend to score higher
        num_ppl_really_like = round(self.num_townspeople * self.frac_upvoting)

        #number of people that tend to score lower
        num_ppl_really_dislike = round(self.num_townspeople * self.frac_downvoting)

        #num_ppl_neutral tend to score people fairly
        num_ppl_neutral = self.num_townspeople - num_ppl_really_like - num_ppl_really_dislike
        
        return num_ppl_really_like, num_ppl_really_dislike, num_ppl_neutral


    def create_personas(self):
        """This function creates a dictionary with each personas
        mean offset and standard deviation.

        Returns:
            Dictionary
        """
        #create the personas:
        personas = {}
        counter = 0
        for n in range(self.num_ppl_neutral):
            this_persona = Townsperson(counter, self.st_dev, 'reasonable')
            personas[this_persona.number] = {}
            personas[this_persona.number]['mean_offset'] = this_persona.mean_offset
            personas[this_persona.number]['std'] = this_persona.std
            counter+=1

        for n in range(self.num_ppl_really_like):
            this_persona = Townsperson(counter, self.st_dev, 'upvoting')
            personas[this_persona.number] = {}
            personas[this_persona.number]['mean_offset'] = this_persona.mean_offset
            personas[this_persona.number]['std'] = this_persona.std
            counter+=1

        for n in range(self.num_ppl_really_dislike):
            this_persona = Townsperson(counter, self.st_dev, 'downvoting')
            personas[this_persona.number] = {}
            personas[this_persona.number]['mean_offset'] = this_persona.mean_offset
            personas[this_persona.number]['std'] = this_persona.std
            counter+=1
        return personas


    def compute_score(self, objective_score, persona, incremental_number, random_seed = False):
        """This function computes the subjective score.

        Args:
            objective_score (float): guac god given score
            persona (dictionary): persona's mean offset and standard deviation
            incremental_number (int): guac incremental number for the fullness factor

        Returns:
            float: the subjective score
        """
        mean = objective_score + persona['mean_offset']
        std = persona['std']

        #The fullness factor is fit with a straight line from 0 at the first guac to -2 at the last guac
        if self.fullness_factor:
            ff = (-2.0/self.num_guacs_per_voter)*incremental_number
            mean += ff

        if random_seed:
            np.random.seed(10)

        subjective_score = round(np.random.normal(mean, std), 1)
        if subjective_score > 10: 
            subjective_score = 10
        if subjective_score < 0:     
            subjective_score = 0
        return subjective_score


    def declare_winner(self, metric):
        """This function computes the winners and winner based on some metric

        Args:
            metric (string): metric to use

        Returns:
           a list of winner and the randomly chosen one
        """
        if metric == 'sum':

            sorted_scores = self.results_df.sort_values(by='sum', ascending=False)

            #extract highest sum        
            winning_sum = sorted_scores.iloc[0]['sum']

            #To carch multiple winners, create a dictionary of sums - winners
            sum_winners_dict = utils.create_map_one_to_many(sorted_scores, 'sum', 'id')
            
            sum_winners = sum_winners_dict[winning_sum]

            if len(sum_winners) > 1:
                print("\n\n\nMultiple sum winners, picking one at random...\n\n\n")
                
            return sum_winners, sum_winners[0]

        elif metric == 'condorcet':

            #creating the list that will contain each matrix ballot
            ballots_matrix_list = []

            for col in self.scores_cols:

                #Select the votes for each persona and compute the condorcet elements
                sample_guac_df = self.results_df[['id', col]].rename(columns={col:'subjective_score'})
                sample_guac_df = sample_guac_df[~sample_guac_df['subjective_score'].isnull()]
                condorcet_elements = Condorcetcounting(self.guac_df, sample_guac_df)

                #collect ballox matrices
                ballots_matrix_list.append(condorcet_elements.ballot_matrix)
            
            return condorcet_elements.get_winners(self.results_df, ballots_matrix_list)

        else:
            sys.exit(f"Unknown metric {metric} to calculate winner...") 


    def simulate(self, winner_metric):
        """This function computes the subjective scores for all guacs.

        Args:
            winner_metric (string): type of metric used to determine the winner
        """
        
        #collect people scores
        self.results_df = self.guac_df.copy()        
        
        self.scores_cols = []

        for persona in self.personas.keys():
            #new column name
            this_col = f"subjective_score_{persona}"

            #select a subset of guacs to score
            random_sample_df = self.results_df[['id', 'objective_score']].sample(n=self.num_guacs_per_voter, replace=False)

            #add incremendal number for fullness score
            random_sample_df['incremendal_number'] = range(1, len(random_sample_df)+1)

            #assign the subjective score
            random_sample_df[this_col] = random_sample_df.apply(lambda x: self.compute_score(x['objective_score'], 
                                                                                            self.personas[persona], 
                                                                                            x['incremendal_number']), 
                                                                                            1)
            #get the id-score map
            id_score_map = dict(zip(random_sample_df['id'].tolist(), random_sample_df[this_col].tolist()))

            #collect scores into dataframe
            self.results_df[this_col] = self.results_df['id'].apply(lambda x: id_score_map.get(x, None))
  
            #collect columns with scores
            self.scores_cols.append(this_col)
        
        self.results_df['sum'] = self.results_df[self.scores_cols].sum(axis=1)
        self.results_df['mean'] = self.results_df[self.scores_cols].mean(axis=1)

        #find the winners
        self.winners, self.winner = self.declare_winner(winner_metric)
        
        


