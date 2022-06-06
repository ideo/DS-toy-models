from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
import numpy as np
from mesa import Model
from .neighbor import Neighbor
import random

class Interact(Model):
    def __init__(self, 
                n_neighbors, 
                n_already_composting, 
                personality_spread, 
                personality_xmax, 
                sociability_spread,
                encouragement_skew, 
                encouragement_xmax, 
                openness_skew,
                openness_xmax,
                days,
                seed = None):

        # We consider 30 days in total. In each day, 
        # the number of ticks = number of people in the neighborhood. 
        # then during each tick, a single person gets the opportunity to “match” 
        # with another person who isn’t already matched. 
        # Then once everyone has gotten a chance to match 
        # (i.e. when the tick is a multiple of the number of people in the neighborhood) 
        # the day restarts.
        self.ticks = days * n_neighbors  
        self.current_tick = 1

        # activate all agents at once
        self.schedule = SimultaneousActivation(self)  

        #list of agents
        self.neighbors = []
        self.n_neighbors = n_neighbors
        self.n_already_composting = n_already_composting
        
        self.personality_spread = personality_spread
        self.personality_xmax = personality_xmax

        self.sociability_spread = sociability_spread
        
        self.encouragement_skew = encouragement_skew
        self.encouragement_xmax = encouragement_xmax

        self.openness_skew = openness_skew
        self.openness_xmax = openness_xmax

        self.seed = seed

        # Setting up a data collector to track metrics of interest at every step
        # of the simulation.
        # This is invoked via .collect(model), so the model in the lambda function
        # is the input model.
        self.datacollector = DataCollector(
            model_reporters = {
                # "agent_count": lambda m: m.schedule.get_agent_count(),
                'neighborhood_size': lambda m: m.n_neighbors,
                'personality_spread': lambda m: m.personality_spread,
                'sociability_spread': lambda m: m.sociability_spread,
                'encouragement_skew': lambda m: m.encouragement_skew,
                'openness_skew': lambda m: m.openness_skew,
                'initial_number_of_composters': lambda m: m.n_already_composting,
                'number_of_composters': self.data_collector_get_composters
            })
        if self.seed is not None:
            np.random.seed(self.seed)
            random.seed(self.seed)

        self.create_neighbor_agents()

        # testing to figure out why graph not updating when you change personality spread or sociability margin
        # print([n.personality for n in self.neighbors])
        # print([n.sociability_margin for n in self.neighbors])
        # print([n.encouragement for n in self.neighbors])

    def create_neighbor_agents(self):
        """This function creates the neighbor agents
        """
        
        # holds neighbor agents
        self.neighbors = []  

        # randomly pick people who are already composting
        who_already_composting = np.random.choice(self.n_neighbors, self.n_already_composting, replace = False)
        print(who_already_composting)
        
        for n in range(self.n_neighbors):

            #the neighbor object needs a unique id (n) and the interaction model (self)
            neighbor = Neighbor(n, self)
            self.schedule.add(neighbor)
            self.neighbors.append(neighbor)            
            if n in who_already_composting:
                self.neighbors[n].compost = True
                print(n)
            print(sum([n.compost for n in self.neighbors]), n)



    def reset_match_status(self):
        """ This function resets the matched status and make everyone available to chat again.
        """
        for n in range(self.n_neighbors):
            self.neighbors[n].matched_for_conversation = False
        # print(f"********************")
        # print(f"It's day {self.current_tick / self.n_neighbors} -> reset availability of neighbors")
        #
        # print(f"********************")


    def step(self):
        """This function tells the scheduler to move 1 step forward, 
        at which point, the step() function of all agents are called.
        """
        # If the step is a multiple of the total number of neighbors,
        # it means that every person is on the same day. 
        # We thus reset matched status and make everyone available to chat again.
        if self.current_tick % self.n_neighbors == 0:
            self.reset_match_status()
            # print(sum([n.compost for n in self.neighbors]))

        # data collection
        self.datacollector.collect(self)
        self.schedule.step()
        self.current_tick += 1

    @staticmethod
    def data_collector_get_composters(model):
        """This function collects the number of people who compost

        Args:
            model (mesa model)

        Returns:
            int: number of people who compost.
        """
        return sum([n.compost for n in model.neighbors])




