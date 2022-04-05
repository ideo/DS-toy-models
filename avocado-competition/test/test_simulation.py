#python -m pytest
import pandas as pd
import numpy as np
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

    dummy_df = pd.DataFrame()
    dummy_number = 0
    sim = Simulation(dummy_df, dummy_number, dummy_number)
    df['subjective_score'] = df.apply(lambda x: sim.compute_score(x['objective_score'], 
                                                                        persona, 
                                                                        x['incremendal_number'], 
                                                                        random_seed = True), 
                                                                        1)
                                                                            
    assert df['subjective_score'].tolist() == [1.3, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, 8.3, 9.3, 10.0]

