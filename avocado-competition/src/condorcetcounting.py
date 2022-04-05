'''
A good chunk of this script is courtesy of 
Alex Fink and Russell McClellan
'''
import numpy as np
import pandas as pd
import sys
import os

#importing this file path to load packages
this_file_path = os.path.dirname(__file__)
sys.path.append(this_file_path)

import utils as utils

class Condorcetcounting():
    def __init__(
            self, 
            guac_df, 
            sample_guac_df):
        
        #list of winners
        self.winners=[]
        
        #randomly selected winner
        self.winner=None

        #dataframe containing the set ot winners
        self.smith_schwartz_set_df=pd.DataFrame()

        #dataframe containing all the guacs
        self.guac_df = guac_df
        
        #list of guacs IDs
        self.guac_names = list(guac_df['id'])
        
        #number of guacs in the competition
        self.num_guacs = len(guac_df)
        
        #dataframe with a sample of guacs
        self.sample_guac_df = sample_guac_df
        
        #dictionary with guac ID and score
        self.ballot_dict = self.get_ballot_dictionary()        
        
        #numpy matrix of wins
        self.ballot_matrix = self.create_ballot_matrix()
                    

    def create_ballot_matrix(self):
        """This function converts a ballot containing a score for each guac into
        a matrix of runner (rows) vs opponent (columns), where wins (and only wins) are marked as 1.

        Returns:
            numpy ballot matrix
        """
        
        # Create the ballot matrix, row by row.
        ballot_matrix = []

        #loop on runners
        for runner in self.guac_names:   

            #if this runner wasn't in the ballot, then fill in with 0s and move to the next
            if runner not in self.ballot_dict.keys():
                ballot_matrix.append([0 for i in range(len(self.guac_names))])
                continue

            ballot_array = []
            #loop on opponents
            for opponent in self.guac_names:

                #if this opponent wasn't in the ballot, add a 0 and move to the next
                if opponent not in self.ballot_dict.keys():
                    ballot_array.append(0)
                    continue
                    
                #if runner beats the opponent, record the win
                if self.ballot_dict[runner] > self.ballot_dict[opponent]:
                    ballot_array.append(1)
                else: 
                    ballot_array.append(0)

            #append to then create a ballot matrix
            ballot_matrix.append(ballot_array)
    
        ballot_matrix = np.matrix(ballot_matrix)

        return ballot_matrix


    def get_ballot_dictionary(self):
        """This function extract a dictionary with guac and vote

        Returns:
            guac:vote dictionary
        """
        ballot_dict = dict(zip(self.sample_guac_df['id'], self.sample_guac_df['subjective_score']))         
        return ballot_dict

    def get_schwartz_relations_matrix(self, sum_ballots_matrix):
        """This function creates a matrix of the preferences.
         True is in positions where a runner is preferred more than the opponent.

        Args:
            sum_ballots_matrix (numpy matrix): matrix containing the sums of all the wins

        Returns:
            matrix of preferences
        """
        #initialize a matrix with all zeros 
        matrix_of_more_preferred = np.zeros([self.num_guacs,self.num_guacs], dtype=np.bool) # Init to False (loss)
        #loop through all guacs and check the runner vs opponent preferences. 
        #when the runner is more preferred than the opponent (by more votes), flip the matrix location to True
        for runner in range(self.num_guacs):
            for opponent in range(self.num_guacs):
                if runner == opponent: continue
                if (sum_ballots_matrix[runner][opponent] > sum_ballots_matrix[opponent][runner]):
                    matrix_of_more_preferred[runner][opponent] = True # Victory (no tie)

        return matrix_of_more_preferred

    def get_smith_or_schwartz_set_statuses(self, matrix_of_more_preferred):
        """Uses Floyd-Warshall algorithm to find out which candidates are in the Smith or Schwartz Set.
        The set returned is dependent on the calculation of the relations.
        Modeled after https://wiki.electorama.com/wiki/Maximal_elements_algorithms

        Args:
            matrix_of_more_preferred (numpy matrix): matrix containing True when a runner is preferred more than the opponent.

        """
        #assume every guac belongs, then knock them off
        is_in_smith_or_schwartz_set = np.ones(self.num_guacs,dtype=np.bool) #Init to True

        # Use transitive properties to determine winners. 
        # E.g., if B > A and A > C then B > C
        matrix_of_more_preferred_tp = matrix_of_more_preferred.copy()
        for runner in range(self.num_guacs):
            for opponent in range(self.num_guacs):
                if runner != opponent:
                    for middle_guac in range(self.num_guacs):
                        if ((runner != middle_guac) and (opponent != middle_guac)):
                            if (matrix_of_more_preferred_tp[opponent][runner] and matrix_of_more_preferred_tp[runner][middle_guac]):
                                matrix_of_more_preferred_tp[opponent][middle_guac] = True
        
        for runner in range(self.num_guacs):
            for opponent in range(self.num_guacs):
                if (runner != opponent):
                    if (matrix_of_more_preferred_tp[opponent][runner] and not matrix_of_more_preferred_tp[runner][opponent]):
                        is_in_smith_or_schwartz_set[runner] = False
                        break
        smith_schwartz_set_df = pd.DataFrame(index = self.guac_names)
        smith_schwartz_set_df['in_set'] = is_in_smith_or_schwartz_set
        return smith_schwartz_set_df
        
    def get_winners(self,results_df, ballots_matrix_list, metric='mean'):
        """This function computes the condorcet winner by ranking the guacs
        belonging to the smith set and ranking them by their average score

        Args:
            results_df (dataframe): dataframe with the scores
            ballots_matrix_list (list): list of numpy matrices
        Returns:
            winning guac
        """
        #sum all ballot matrices
        ballot_matrices_sum = self.sum_ballot_matrices(ballots_matrix_list)

        #find the runners more preferred
        matrix_of_more_preferred = self.get_schwartz_relations_matrix(ballot_matrices_sum)

        #find the sets of winners and loosers
        self.smith_schwartz_set_df = self.get_smith_or_schwartz_set_statuses(matrix_of_more_preferred)
        
        #add to the sets of winners and loosers the mean to find the absolute winner
        results_df.index = results_df['id']
        self.smith_schwartz_set_df = self.smith_schwartz_set_df.join(results_df[['mean']]) 
        self.smith_schwartz_set_df['id'] = self.smith_schwartz_set_df.index

        #filter out the winners
        winners_df = self.smith_schwartz_set_df[self.smith_schwartz_set_df['in_set'] == True].copy()
        winners_df.sort_values(by = [metric], ascending = False, inplace = True)

        #if there's no winner
        if len(winners_df)  == 0: sys.exit("No condorcet winner")         
        
        #get the winning mean
        winning_mean = winners_df.iloc[0][metric]
        
        #create a dictionary of means - winners to catch multiple winners
        mean_winners_dict = utils.create_map_one_to_many(winners_df, metric, 'id')

        #extract the winners from the dictionary
        winners = mean_winners_dict[winning_mean]

        if len(winners) > 1:
            print("\n\n\nMultiple condorcet winners, picking one at random...\n\n\n")
            
        return winners, winners[0]



    def sum_ballot_matrices(self, ballots_matrix_list):
        """This function sums all the ballot matrices

        Args:
            ballots_matrix_list (list): list of numpy matrices

        Returns:
            numpy matrix containing the sum of matrix ballots
        """
        null_matrix = np.zeros([len(self.guac_df),len(self.guac_df)])
        
        ballots_matrix_sum = null_matrix.copy()
        
        for bm in ballots_matrix_list:
            ballots_matrix_sum += bm

        if np.array_equal(ballots_matrix_sum, null_matrix) == True:
            sys.exit("Ballot matrix sum is null, something is wrong...") 

        return ballots_matrix_sum
