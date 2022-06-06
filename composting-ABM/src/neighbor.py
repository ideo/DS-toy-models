from os import stat
import numpy as np
import altair as alt
import random
import src.utils as utils

from mesa import Agent, Model
from mesa.time import SimultaneousActivation, RandomActivation
from mesa.datacollection import DataCollector


class Neighbor(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        self.unique_id = unique_id
        self.compost = False
        # self.compost = self.assign_if_compost(model)

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

        # each neighbor has openness parameter, which is their probability of trying composting if they're encouraged
        self.openness = utils.sample_from_beta_distr(dummy_val, 
                                                        model.openness_xmax, 
                                                        model.openness_skew, 
                                                        False)
        # whether or not they're matched with a conversational partner
        self.matched_for_conversation = False 

    # def assign_if_compost(self, model):  # removed this because we had duplicate methods of determining how many people composted
    #     """This function determines whether a neighbor composts.
    #     If a random seed is assigned, the list of IDs that composts is fixed
    #     otherwise it is randomly generated
    #
    #     Args:
    #         mesa model
    #     """
    #
    #     '''
    #     if model.seed is not None:
    #         np.random.seed(model.seed)
    #         random.seed(model.seed)
    #     '''
    #
    #     composters_list = random.sample(range(model.n_neighbors), 10)
    #
    #     return True  if self.unique_id in composters_list else False
        

        
    def step(self):
        """This method describes what do they do at each step (tick) 
        of the simulation.
        """
        # Each day has n_neighbors ticks.
        # Each neighbor has a "turn" to interact when the 
        # current tick modulo the number of agents is the neighbor's ID, provided
        # it wasn't matched for a convo already.
        if self.model.current_tick % self.model.n_neighbors == self.unique_id and \
            not self.matched_for_conversation:
            neighbor = self.find_a_match()
            if self.matched_for_conversation:
                self.talk(neighbor)

    # TODO: make attempts_limit a parameter people can play with in a side bar
    def find_a_match(self, attempts_limit = 5):
        """ This function finds a match for neighbors that aren't matched yet
        """
        
        # list of other and unmatched neighbors to talk to:
        potential_partners = [n for n in self.model.neighbors \
                                if n.unique_id != self.unique_id \
                                and not n.matched_for_conversation]
        
        #if there are no potential partners do nothing.
        if len(potential_partners) == 0: pass

        # print(f"self: {self.unique_id}, potential_partners: {[n.unique_id for n in potential_partners]}")

        # For simplicity, let's limit the interaction to 5 people
        attempts = min(attempts_limit, len(potential_partners))  
                
        for i in range(attempts):            
            
            # Pick a neighbor at random
            neighbor = np.random.choice(potential_partners)  

            # Check if self and neighbor are compatible (i.e., if their personalities windows overlap)
            # If so, mark them as matched and break the loop
            if self.check_personalities_overlap(neighbor):

                # print(f"tick {self.model.current_tick} - {self.unique_id} matched with {neighbor.unique_id}")
                self.matched_for_conversation = True
                self.model.neighbors[neighbor.unique_id].matched_for_conversation = True
                return neighbor
            else:
                # if it's not a mach, remove the neighbor from the list of potential partners and move to the next
                potential_partners.remove(neighbor)
        
        return None
            
    
    def talk(self, neighbor): 
        """This function process the interaction between self and the neighbor and 
        computes if either one converts to composting or not.

        Args:
            neighbor agent
        """
        
        #if either both already compost or both don't, then nothing happens
        if (neighbor.compost and self.compost) or \
           (not neighbor.compost and not self.compost): 
           pass
        
        # if neighbor already composts but self doesn't:
        if neighbor.compost and not self.compost:
            if self.will_convert(neighbor, self):
                self.compost = True
        
        # if neighbor doesn't compost but self does:
        elif not neighbor.compost and self.compost:  
            if self.will_convert(self, neighbor):
                neighbor.compost = True    
    
    @staticmethod
    def will_convert(encourager, candidate_to_compost):
        """ This function uses 1) the encourager probability to determine
        if they talk about composting and 2) the candidate openness probability 
        to determine if they'll convert to compost.

        Args:
            encourager (neighbor object)
            candidate_to_compost (neighbor object)

        Returns:
            boolean on whether conversion occurs.
        """
        encourage = np.random.binomial(1, encourager.encouragement)
        convert = np.random.binomial(1, candidate_to_compost.openness)

        if encourage == 1 and convert == 1:
            return True
        else:
            False


    def check_personalities_overlap(self, neighbor):
        """This function computes the personality window of self and
        a neighbor and check for overlap

        Args:
            neighbor (object)

        Returns:
            boolean: whether the personalities of self and neighbor overlap
        """
        # Check if their personalities windows overlap
        self_window = [self.personality - self.sociability_margin, 
                       self.personality + self.sociability_margin]

        neighbor_window = [neighbor.personality - neighbor.sociability_margin, 
                           neighbor.personality + neighbor.sociability_margin]
        
        return self.ranges_intersect(self_window, neighbor_window)


    @staticmethod
    def ranges_intersect(a, b):
        """This function checks if two intervals overlap

        Args:
            a (tuple): interval 1
            b (tuple): interval 2

        Returns:
            boolean on whether the intervals overlap

        a0|------------|a1
            b0|-----------------|b1

            a0|------------|a1
         b0|------|b1


        """

        if (a[0] <= b[1] and a[1] >= b[0]) or (b[0] <= a[1] and b[1] >= a[0]):
            return True
        else: 
            return False

