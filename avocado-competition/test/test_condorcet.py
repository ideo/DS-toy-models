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

def test_sum_ballot_matrices():
    """This function tests the sum of matrices using Jenna's ballots.
    """

    dummy, dummy, ballot_matrices_sum = get_jenna_ballot_matrices_sum()
    expected_matrix = np.matrix([[0, 0, 0, 2, 0, 0],
                                 [3, 0, 0, 3, 1, 0],
                                 [1, 1, 0, 2, 1, 2],
                                 [1, 1, 0, 0, 1, 0],
                                 [1, 1, 2, 2, 0, 1],
                                 [1, 1, 1, 2, 2, 0]])

    assert np.array_equal(ballot_matrices_sum, expected_matrix)


def test_get_schwartz_relations_matrix():
    condorcet_elements, dummy, ballot_matrices_sum = get_jenna_ballot_matrices_sum()
    matrix_of_more_preferred = condorcet_elements.get_schwartz_relations_matrix(ballot_matrices_sum)

    expected_matrix = np.matrix([[False, False, False,  True, False, False],
                                [ True, False, False,  True, False, False],
                                [ True,  True, False,  True, False,  True],
                                [False, False, False, False, False, False],
                                [ True, False,  True,  True, False, False],
                                [ True,  True, False,  True,  True, False]])

    assert np.array_equal(matrix_of_more_preferred, expected_matrix)


def test_get_smith_or_schwartz_set_statuses():
    condorcet_elements, dummy, ballot_matrices_sum = get_jenna_ballot_matrices_sum()
    matrix_of_more_preferred = condorcet_elements.get_schwartz_relations_matrix(ballot_matrices_sum)
    smith_schwartz_set_df = condorcet_elements.get_smith_or_schwartz_set_statuses(matrix_of_more_preferred)

    assert smith_schwartz_set_df['in_set'].tolist() == [False, False,  True, False,  True,  True]

def test_get_winner():
    condorcet_elements, ballot_matrices_list, dummy = get_jenna_ballot_matrices_sum()
    # condorcet_elements.get_winners(pd.DataFrame(), ballot_matrices_list)
    #FIXME from here. Add the last test
    """
       id  objective_score    color  subjective_score_0  subjective_score_1  subjective_score_2  subjective_score_3  ...  subjective_score_195  subjective_score_196  subjective_score_197  subjective_score_198  subjective_score_199    sum      mean
0   0                4  #4c78a8                 2.4                 6.6                 NaN                 NaN  ...                   0.0                   0.0                   0.0                   0.5                   NaN  283.2  2.832000
1   1                5  #4c78a8                 NaN                 0.9                 2.2                 3.2  ...                   NaN                   0.0                   NaN                   2.7                   3.0  379.1  3.791000
2   2                2  #4c78a8                 3.4                 NaN                 NaN                 1.1  ...                   1.2                   NaN                   0.0                   NaN                   NaN  148.4  1.400000
3   3                7  #4c78a8                 NaN                 NaN                 NaN                 3.9  ...                   NaN                   2.8                   NaN                   0.3                   NaN  558.5  5.757732
4   4                6  #4c78a8                 5.0                 7.2                 NaN                 2.5  ...                   0.0                   3.1                   5.2                   1.3                   3.1  436.4  4.545833


    """


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

def get_jenna_ballot_matrices_sum():
    """This function creates the matrix containing the sum of Jenna's ballots

    Returns:
        condorcet elements
        matrix containing the sum of Jenna's ballots
        list of ballot matrices        
    """

    ballots_matrix_list = []
    guac_df = get_jennas_guac_df()

    for townsperson in range(7):
        sample_guac_df = get_jennas_sample_guac_df(townsperson)
        sample_guac_df = sample_guac_df[~sample_guac_df['subjective_score'].isnull()]
        condorcet_elements = Condorcetcounting(guac_df, sample_guac_df)

        #collect ballox matrices
        ballots_matrix_list.append(condorcet_elements.ballot_matrix)

    ballot_matrices_sum = condorcet_elements.sum_ballot_matrices(ballots_matrix_list)
    return condorcet_elements, ballots_matrix_list, ballot_matrices_sum


