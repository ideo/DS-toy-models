#python -m pytest
import pandas as pd
import numpy as np
import sys
import os

    #create matrix sum and check
    #create preference matrix and check
    #create next matrix and check
    #create swarz set and check
    #find winners and check

#adding to the known directory the one where the script sits
this_file_path = os.path.dirname(__file__)
script_path = os.path.join(this_file_path, '..')
sys.path.append(script_path)

from src.condorcetcounting import Condorcetcounting

'''
        if TEST_JENNAS_NUMBERS:
            self.num_townspeople = 7
            self.assigned_guacs = 6
            self.guac_df = pd.DataFrame([0,1,2,3,4,5], columns = ['Entrant'])
            self.guac_df['Objective Ratings'] = 0

        if self.test_jennas_numbers:

        condorcet_elements = Condorcetcounting(guac_df, sample_guac_df)
        return condorcet_elenments

'''

def get_condorcet_elements(townsperson):
    guac_df = get_jennas_guac_df()
    guac_sample_df = get_jennas_sample_guac_df(townsperson)
    return Condorcetcounting(guac_df, guac_sample_df)


def test_create_ballot_dict():

    townsperson = 0
    condorcet_elements = get_condorcet_elements(townsperson)

    expected_dictionary = {2: 2, 4: 3, 5: 1}
    assert condorcet_elements.ballot_dict == expected_dictionary

    townsperson = 3
    condorcet_elements = get_condorcet_elements(townsperson)
    expected_dictionary = {0: 9, 1: 9.5, 2: 10, 3:3}
    assert condorcet_elements.ballot_dict == expected_dictionary

def test_create_ballot_matrix():
    townsperson = 0
    
    condorcet_elements = get_condorcet_elements(townsperson)

    expected_matrix = np.matrix([[0,0,0,0,0,0], 
                                [0,0,0,0,0,0], 
                                [0,0,0,0,0,1], 
                                [0,0,0,0,0,0], 
                                [0,0,1,0,0,1], 
                                [0,0,0,0,0,0]])
    assert np.array_equal(condorcet_elements.ballot_matrix, expected_matrix)

    townsperson = 3
    
    condorcet_elements = get_condorcet_elements(townsperson)

    expected_matrix = np.matrix([[0,0,0,1,0,0], 
                                [1,0,0,1,0,0], 
                                [1,1,0,1,0,0], 
                                [0,0,0,0,0,0], 
                                [0,0,0,0,0,0], 
                                [0,0,0,0,0,0]])
    assert np.array_equal(condorcet_elements.ballot_matrix, expected_matrix)


def get_jennas_guac_df():
    """This function creates a dataframe containing all guacs

    Returns:
        dataframe
    """
    guac_df = pd.DataFrame([0,1,2,3,4,5], columns = ['id'])
    guac_df['objective_score'] = 0
    return guac_df
    
def get_jennas_sample_guac_df(townperson):
    """This function returns a dataframe with subjective ratings for 
    a given townperson

    Args:
        townperson (int): townperson ID

    Returns:
        dataframe of the form:

        id  subjective_ratings
     0   2                   2
     1   4                   3
     2   5                   1
    
    """

    row = {}
    row[0] = [(2,2), (4,3), (5,1)]
    row[1] = [(2,2), (4,5), (5,10)]
    row[2] = [(2,7),(3,2), (4,3.3), (5,4)]
    row[3] = [(0,9), (1,9.5), (2,10), (3,3)]
    row[4] = [(0,9), (1,9.5), (3,0), (5,10)]
    row[5] = [(1,5), (3,4), (4,8)]
    row[6] = [(0,6),(1,8),(3,10),(4,7)]    
    return pd.DataFrame(row[townperson], columns = ["id", 'subjective_score'])


    # return pd.DataFrame(jennas_data[self.number], columns = ["id", 'subjective_rating'])
