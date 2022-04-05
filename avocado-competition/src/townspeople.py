# import numpy as np
# import pandas as pd
# from .condorcetcounting import Condorcetcounting


# Base Class
class Townsperson:
    def __init__(
        self, 
        person_number,
        std,  
        person_type='fair', 
        ):#, person_number, fullness_factor = 0.0, st_dev=1, 
                # assigned_guacs=20, 
                # min_allowed_vote = 1, max_allowed_vote = 10, 
                # mean_offset=0, carlos_crony=False,
                # test_jennas_numbers = False):
        self.number = person_number
        self.type = person_type
        self.mean_offset = self.get_mean_offset()
        self.std = std
    
    def get_mean_offset(self):
        if self.type == 'upvoting':
            return 2
        elif self.type == 'downvoting':
            return -2
        else:
            return 0
    