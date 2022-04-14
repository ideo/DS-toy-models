import numpy as np
import altair as alt
import random
import src.utils as utils

from mesa import Agent, Model
from mesa.time import SimultaneousActivation, RandomActivation
from mesa.datacollection import DataCollector

def ranges_intersect(a, b):  # function to see if two agents can get along
    if (a[0] <= b[1] and a[1] >= b[0]) or (b[0] <= a[1] and b[1] >= a[0]):
        return True
    else: return False


class Neighbor(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.unique_id = unique_id
        self.compost = self.assign_if_compost(model)

        # neighbor has a personality score which represents "what kind of person they are"        
        dummy_val = 0
        self.personality = utils.sample_from_beta_distr(dummy_val, 
                                                        model.personality_xmax,                                                         
                                                        model.personality_spread, 
                                                        True)

        # there is a sociability margin about each person's personality score--
        # neighbors will only talk to each other if their personality scores 
        # are mutually within each others' margins.
        self.sociability_margin = abs(utils.sample_from_normal_distr(dummy_val, 
                                                                    model.sociability_spread))

        # if talking to another neighbor, each neighbor also has a likelihood of encouraging them to try composting
        self.encouragement = utils.sample_from_beta_distr(dummy_val, 
                                                        model.encouragement_xmax, 
                                                        model.encouragement_skew, 
                                                        False)

        # each neighbor has stubbornness parameter, which is their probability of trying composting if they're encouraged
        self.stubbornness = utils.sample_from_beta_distr(dummy_val, 
                                                        model.stubbornness_xmax, 
                                                        model.stubbornness_skew, 
                                                        False)
        # whether or not they're matched with a conversational partner
        self.matched_for_conversation = False 

    def assign_if_compost(self, model):
        """This function determines whether a neighbor composts. 
        If a random seed is assigned, the list of IDs that composts is fixed
        otherwise it is randomly generated

        Args:
            mesa model
        """                
        if model.seed is not None:
            random.seed(model.seed)

        composters_list = random.sample(range(model.n_neighbors), 10)

        return True  if self.unique_id in composters_list else False
        

    def talk(self):  # find a match and talk to them.
        # list of current options for neighbors to talk to:
        talk_options = [n for n in self.model.neighbors if n.unique_id != self.unique_id and not n.matched_for_conversation]
        # print('self:', self.unique_id, 'options:', [n.unique_id for n in talk_options])
        attempts = min(5, len(talk_options))  # limit attempts to find a convo partner to 5 just for simplicity right now
        neighbor = None
        while not self.matched_for_conversation and attempts > 0:
            if len(talk_options) != 0:  # if there are remaining options for neighbors to interact with:
                neighbor = np.random.choice(talk_options)  # sample randomly from remaining neighbors
                # print('trying', neighbor.unique_id)
                # if their sociability margins overlap:
                self_personality_window = [self.personality - self.sociability_margin, self.personality + self.sociability_margin]
                neighbor_personality_window = [neighbor.personality - neighbor.sociability_margin, neighbor.personality + neighbor.sociability_margin]
                if ranges_intersect(self_personality_window, neighbor_personality_window):  # if they're compatible:
                    # get neighbor's ID
                    neighbor_id = neighbor.unique_id
                    # print('tick', self.model.current_tick, ':', self.unique_id, 'matched with', neighbor_id)
                    # mark self and partner as matched
                    self.matched_for_conversation = True
                    self.model.neighbors[neighbor_id].matched_for_conversation = True
                    talk_options.remove(neighbor)
                else:
                    talk_options.remove(neighbor)
                    neighbor = None  # if not compatible, reset neighbor to none and remove them from options
            if not self.matched_for_conversation:
                attempts -= 1

        # the person who initiates contact is the one who "knows" which neighbor they're matched with
        # so they have to process the transaction
        if neighbor is not None:  # if didn't give up on finding a match after 5 attempts:
            # TODO: maybe turn this into a function since it repeats
            if neighbor.compost and not self.compost:  # if neighbor already composts but self doesn't:
                # use neighbor's encouragement probability to determine if they talk about composting
                encourage = np.random.binomial(1, neighbor.encouragement)
                if encourage == 1:  # if encouraged, self might be converted:
                    convert = np.random.binomial(1, self.stubbornness)
                    if convert == 1:  # if converted, change compost status to True
                        self.compost = True
            elif not neighbor.compost and self.compost:  # if neighbor doesn't compost but self does:
                # use own encouragement probability to determine if self talks about composting
                encourage = np.random.binomial(1, self.encouragement)
                if encourage == 1:  # if encourages neighbor, they might be converted:
                    convert = np.random.binomial(1, neighbor.stubbornness)
                    if convert == 1: # if converted, change compost status to True
                        neighbor.compost = True

        # if either both already compost or both don't, then nothing happens

    def step(self):
        # each neighbor has a "turn" to interact when the current tick modulo the number of agents is the neighbor's index/ID.
        if self.model.current_tick % self.model.n_neighbors == self.unique_id and not self.matched_for_conversation:
            # print(self.unique_id)
            self.talk()
        # make sure they have a way to reset matched status for each step:


