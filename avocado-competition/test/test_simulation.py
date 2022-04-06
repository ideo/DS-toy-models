#python -m pytest
import pandas as pd
import sys
import os

#adding to the known directory the one where the script sits
this_file_path = os.path.dirname(__file__)
script_path = os.path.join(this_file_path, '..')
sys.path.append(script_path)

from src.simulation import Simulation


def test_compute_score():
    #create a dataframe with objective scores
    df = pd.DataFrame(range(10), columns = ['objective_score'])
    persona = {'mean_offset': 0, 'std': 1}
    df['incremendal_number'] = range(1, len(df)+1)

    dummy_sim = get_dummy_simulation()
    df['subjective_score'] = df.apply(lambda x: dummy_sim.compute_score(x['objective_score'], 
                                                                        persona, 
                                                                        x['incremendal_number'], 
                                                                        random_seed = True), 
                                                                        1)
                                                                            
    assert df['subjective_score'].tolist() == [1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, 8.3, 9.3, 10.0]


def test_get_personas_counts():
    dummy_sim = get_dummy_simulation()
    assert dummy_sim.num_ppl_neutral == 80
    assert dummy_sim.num_ppl_really_dislike == 60
    assert dummy_sim.num_ppl_really_like == 60


def get_dummy_simulation():
    dummy_guac_df = pd.DataFrame([(1,1), (1,1)], columns = ['id', 'objective_score'])
    dummy_num_townspeople = 200
    dummy_st_dev = 0
    dummy_pct_ppl_really_like = 30
    dummy_pct_ppl_really_dislike = 30

    return Simulation(dummy_guac_df, dummy_num_townspeople, dummy_st_dev, 
                        pct_ppl_really_like = dummy_pct_ppl_really_like, 
                        pct_ppl_really_dislike = dummy_pct_ppl_really_dislike)
