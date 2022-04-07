#python -m pytest
import pandas as pd
import numpy as np
import sys
import os

#adding to the known directory the one where the script sits
this_file_path = os.path.dirname(__file__)
script_path = os.path.join(this_file_path, '..')
sys.path.append(script_path)

from src.condorcetcounting import Condorcetcounting


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
    condorcet_elements = get_condorcet_elements(0)
    
    ballots_matrix_list, dummy = get_jenna_condorcet_elements()

    ballot_matrices_sum = condorcet_elements.sum_ballot_matrices(ballots_matrix_list)
    
    expected_matrix = np.matrix([[0, 0, 0, 2, 0, 0],
                                 [3, 0, 0, 3, 1, 0],
                                 [1, 1, 0, 2, 1, 2],
                                 [1, 1, 0, 0, 1, 0],
                                 [1, 1, 2, 2, 0, 1],
                                 [1, 1, 1, 2, 2, 0]])

    assert np.array_equal(ballot_matrices_sum, expected_matrix)


def test_get_schwartz_relations_matrix():
    condorcet_elements = get_condorcet_elements(0)
    ballots_matrix_list, dummy = get_jenna_condorcet_elements()
    ballot_matrices_sum = condorcet_elements.sum_ballot_matrices(ballots_matrix_list)
    matrix_of_more_preferred = condorcet_elements.get_schwartz_relations_matrix(ballot_matrices_sum)

    expected_matrix = np.matrix([[False, False, False,  True, False, False],
                                [ True, False, False,  True, False, False],
                                [ True,  True, False,  True, False,  True],
                                [False, False, False, False, False, False],
                                [ True, False,  True,  True, False, False],
                                [ True,  True, False,  True,  True, False]])

    assert np.array_equal(matrix_of_more_preferred, expected_matrix)


def test_get_smith_or_schwartz_set_statuses():
    condorcet_elements = get_condorcet_elements(0)
    ballots_matrix_list, dummy = get_jenna_condorcet_elements()
    ballot_matrices_sum = condorcet_elements.sum_ballot_matrices(ballots_matrix_list)
    matrix_of_more_preferred = condorcet_elements.get_schwartz_relations_matrix(ballot_matrices_sum)
    smith_schwartz_set_df = condorcet_elements.get_smith_or_schwartz_set_statuses(matrix_of_more_preferred)

    assert smith_schwartz_set_df['in_set'].tolist() == [False, False,  True, False,  True,  True]

def test_get_winner():
    condorcet_elements = get_condorcet_elements(0)
    ballots_matrix_list, results_df = get_jenna_condorcet_elements()
    winners, winner = condorcet_elements.get_winners(results_df, ballots_matrix_list)
    assert winner == 5
    assert winners == [5]


def get_jennas_guac_df():
    """This function creates a dataframe containing all of Jenna's guacs

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

def get_jenna_condorcet_elements():
    """This function creates the list of ballot matrices and the results dataframe
    for Jenna's test data

    Returns:
        list of ballot matrices        
        results dataframe
    """

    ballots_matrix_list = []
    guac_df = get_jennas_guac_df()
    results_df = guac_df.copy()

    for townsperson in range(7):
        sample_guac_df = get_jennas_sample_guac_df(townsperson)
        sample_guac_df = sample_guac_df[~sample_guac_df['subjective_score'].isnull()]
        condorcet_elements = Condorcetcounting(guac_df, sample_guac_df)

        #collect ballox matrices
        ballots_matrix_list.append(condorcet_elements.ballot_matrix)

        #collect results
        this_col = f"subjective_score_{townsperson}"
        
        #get the id-score map
        id_score_map = dict(zip(sample_guac_df['id'].tolist(), sample_guac_df['subjective_score'].tolist()))

        #collect scores into dataframe
        results_df[this_col] = results_df['id'].apply(lambda x: id_score_map.get(x, None))

    results_df['mean'] = results_df.mean(axis=1)


    
    return ballots_matrix_list, results_df


def get_condorcet_elements(townsperson):
    """This function returns a condorcetcounting object

    Args:
        townsperson (int): a person ID

    Returns:
        condorcetcounting object
    """
    guac_df = get_jennas_guac_df()
    guac_sample_df = get_jennas_sample_guac_df(townsperson)
    return Condorcetcounting(guac_df, guac_sample_df)

