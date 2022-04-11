import numpy as np
import altair as alt
import altair_viewer as altv
# import pandas as pd
# import random


from mesa import Agent, Model
from mesa.time import SimultaneousActivation, RandomActivation
from mesa.datacollection import DataCollector

def ranges_intersect(a, b):  # function to see if two agents can get along
    if (a[0] <= b[1] and a[1] >= b[0]) or (b[0] <= a[1] and b[1] >= a[0]):
        return True
    else: return False

# functions for data collection:
def get_composters(model):
    return sum([n.compost for n in model.neighbors])

def get_neighborhood_size(model):
    return model.n_neighbors

def get_personality_spread(model):
    return model.personality_spread

def get_sociability_spread(model):
    return model.sociability_spread

def get_encouragement_beta(model):
    return [model.encouragement_beta_a, model.encouragement_beta_b]

def get_stubbornness_beta(model):
    return [model.stubbornness_beta_a, model.stubbornness_beta_b]




class Neighbor(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        # whether or not they compost
        # TODO: on tick 1, I'm trying to randomly select some people who already compost
        self.compost = False

        # neighbor has a personality score which represents "what kind of person they are"
        self.personality = np.random.beta(11 - self.model.personality_spread, 11 - self.model.personality_spread)*10

        # there is a sociability margin about each person's personality score--
        # neighbors will only talk to each other if their personality scores are mutually within each others' margins.
        self.sociability_margin = abs(np.random.normal(0, self.model.sociability_spread))

        # if talking to another neighbor, each neighbor also has a likelihood of encouraging them to try composting
        self.encouragement = np.random.beta(self.model.encouragement_beta_a, self.model.encouragement_beta_b)  # TODO: make these parameters manipulable eventually

        # each neighbor has stubbornness parameter, which is their probability of trying composting if they're encouraged
        self.stubbornness = np.random.beta(self.model.stubbornness_beta_a, self.model.stubbornness_beta_b)

        # whether or not they're matched with a conversational partner
        self.matched = False  # defines whether they have a conversational partner yet


    def talk(self):  # find a match and talk to them.
        # list of current options for neighbors to talk to:
        talk_options = [n for n in self.model.neighbors if n.unique_id != self.unique_id and not n.matched]
        print('self:', self.unique_id, 'options:', [n.unique_id for n in talk_options])
        attempts = min(5, len(talk_options))  # limit attempts to find a convo partner to 5 just for simplicity right now
        neighbor = None
        while not self.matched and attempts > 0:
            if len(talk_options) != 0:  # if there are remaining options for neighbors to interact with:
                neighbor = np.random.choice(talk_options)  # sample randomly from remaining neighbors
                print('trying', neighbor.unique_id)
                # if their sociability margins overlap:
                self_personality_window = [self.personality - self.sociability_margin, self.personality + self.sociability_margin]
                neighbor_personality_window = [neighbor.personality - neighbor.sociability_margin, neighbor.personality + neighbor.sociability_margin]
                if ranges_intersect(self_personality_window, neighbor_personality_window):  # if they're compatible:
                    # get neighbor's ID
                    neighbor_id = neighbor.unique_id
                    print('tick', self.model.current_tick, ':', self.unique_id, 'matched with', neighbor_id)
                    # mark self and partner as matched
                    self.matched = True
                    self.model.neighbors[neighbor_id].matched = True
                    talk_options.remove(neighbor)
                else:
                    talk_options.remove(neighbor)
                    neighbor = None  # if not compatible, reset neighbor to none and remove them from options
            if not self.matched:
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
        if self.model.current_tick % self.model.n_neighbors == self.unique_id and not self.matched:
            # print(self.unique_id)
            self.talk()
        # make sure they have a way to reset matched status for each step:


class Interact(Model):
    def __init__(self, n_neighbors, n_already_composting, personality_spread, sociability_spread,
                 encouragement_beta_a, encouragement_beta_b,
                 stubbornness_beta_a, stubbornness_beta_b, days,
                 seed = None):
        self.ticks = days * n_neighbors  # each neighbor gets one chance at matching oer day; it's a new day when matching statuses reset
        self.current_tick = 1
        self.schedule = SimultaneousActivation(self)  # activate all agents at once
        self.n_neighbors = n_neighbors
        self.n_already_composting = n_already_composting
        self.personality_spread = personality_spread
        self.sociability_spread = sociability_spread
        self.encouragement_beta_a = encouragement_beta_a
        self.encouragement_beta_b = encouragement_beta_b
        self.stubbornness_beta_a = stubbornness_beta_a
        self.stubbornness_beta_b = stubbornness_beta_b
        self.seed = seed
        self.datacollector = DataCollector(
            model_reporters = {
                'Neighborhood Size': get_neighborhood_size,
                'Personality Spread': get_personality_spread,
                'Sociability Spread': get_sociability_spread,
                'Encouragement Beta Parameters:': get_encouragement_beta,
                'Stubbornness Beta Parameters': get_stubbornness_beta,
                'Number of Composters': get_composters
            })

        if self.seed is not None:
            np.random.seed(self.seed)
        self.neighbors = []  # holds neighbor agents
        # randomly choose one person to already be composting
        who_already_composting = np.random.choice(range(self.n_neighbors), self.n_already_composting)
        for n in range(self.n_neighbors):
            neighbor = Neighbor(n, self)
            self.schedule.add(neighbor)
            self.neighbors.append(neighbor)
            if n in who_already_composting:
                self.neighbors[n].compost = True


    def step(self):  # tell the scheduler to move one step forward
        # if the step is a multiple of the total number of neighbors, reset matched status (make everyone available to chat again)
        if self.current_tick % self.n_neighbors == 0:
            for n in range(self.n_neighbors):
                self.neighbors[n].matched = False
            print('day', self.current_tick / self.n_neighbors, 'reset availability of neighbors')

        # data collection
        self.datacollector.collect(self)
        self.schedule.step()
        self.current_tick += 1

'''
model1 = Interact(n_neighbors = 10, personality_spread = 10, sociability_spread = 1,
                  encouragement_beta_a = 3, encouragement_beta_b = 4,
                  stubbornness_beta_a = 5, stubbornness_beta_b = 3,
                  days = 30, seed = 1102
                  )
# TODO: how to make it run until a certain condition is met? see run_model in documentation

for current_tick in range(model1.ticks):
    model1.step()
    # print([n.compost for n in model1.neighbors])

model1_data = model1.datacollector.get_model_vars_dataframe().reset_index()
# print(model1_data)

alt.Chart(model1_data).mark_line().encode(x = 'index', y = 'Number of Composters').show()
'''

# TODO: one potential theme to explore: do we achieve faster collective adaptation of a behavior if a bunch of
#  individuals already behave a certain way but don't talk to each other, as opposed to only a few people behaving a
#  certain way but them having more networked influence?