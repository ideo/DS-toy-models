import streamlit as st
import altair as alt
# TODO: one potential theme to explore: do we achieve faster collective adaptation of a behavior if a bunch of
#  individuals already behave a certain way but don't talk to each other, as opposed to only a few people behaving a
#  certain way but them having more networked influence?
# TODO: add README

import pandas as pd
import src.utils as utils
from src.interact import Interact
st.set_page_config(layout = 'wide')


st.header('How quickly can a neighborhood adopt the practice of composting their food scraps?')
st.write("""People like to pat themselves on the back when they start 
        doing something eco-friendly like composting, but how impactful 
        is an isolated individual partaking in a positive behvior vs. a social individual spreading
        the positive behavior through their network? 
        Tinker with the parameters representing neighbors' willingness
        to encourage others to compost, and their willingness to try composting 
        if encouraged, to see how close the neighborhood gets to completely converting 
        to composting within a 30-day period. 
        Several neighbors are already composting at the start of each simulation. 
        Each day, neighbors randomly meet other neighbors and decide to pair up and 
        chat if their personalities are compatible. What conditions are necessary for 
        composting to really take off in the neighborhood?""")

st.subheader('About some assumptions')
st.write("""For some of the modeling below we use a beta distribution. Our choice is due to its 
convenient shape, being bounded between 0 and 1, and tapering off smoothly at the boundaries.""")

model_plot = None
#initialize the model dataframe to an empty one if not already in the 
#session state.
if 'model_data_frame' not in st.session_state:
    st.session_state["model_data_frame"] = pd.DataFrame()


st.subheader('Choose Your Parameters')
my_cols_tuple = (7, 1, 7, 1, 7)
col1, col2, col3, col4, col5 = st.columns(my_cols_tuple)
with col1:
    # ************************************************************************
    # st.subheader('Random Seed')
    utils.write_custom_subheader('Random Seed')
    seed_input = st.text_input("""Random seed (optional): pick an integer or leave it blank. Choosing a seed ensures that the results 
    will be consistent as long as the same parameter values are chosen.""",
                               key = 'seed_input')

    # Check on random seed. Accept only numbers.
    seed_input = utils.check_random_seed_content(seed_input)
    optional_seed = seed_input if seed_input!= '' else None
    st.write(f"(Random seed = {optional_seed})")

    # TODO: be able to select number of days
    
with col3:
    # ************************************************************************
    # st.subheader('Neighborhood size')
    utils.write_custom_subheader('Neighborhood size')
    neighborhood_size = st.slider('How many people live in the neighborhood?', 
                                    min_value = 10, 
                                    max_value = 200, 
                                    step = 10,
                                    value = 70,
                                    key = 'nbhd')

with col5:
    # ************************************************************************
    # ************************************************************************
    # st.subheader('Fraction of initial composters')
    utils.write_custom_subheader('Fraction of initial composters')
    frac_composters = st.slider('What is the % of composters at the beginning of the simulation?',
                                min_value = 1, 
                                max_value = 50, 
                                value = 10,
                                format="%g%%",
                                key = 'n_composters')
                                
    num_composters = int(frac_composters*neighborhood_size/100)
    print('num composters', num_composters)

my_cols_tuple = (7, 1, 7, 1, 7, 1, 7)
col1, col2, col3, col4, col5, col6, col7 = st.columns(my_cols_tuple)

with col1:
    # ************************************************************************
    # st.subheader('Spread of Personalities')
    utils.write_custom_subheader('Spread of Personalities')
    personality_xmax = 10
    personality_spread = st.slider("""We create personality scores from 1 to 10 assuming 
                                    a symmetric beta distribution and multiplying the result by 10.
                                    Choose the spread of the distribution. You can go all the way 
                                    from narrow (1) to flat (10).""",
                                    min_value = 1, 
                                    max_value = personality_xmax, 
                                    value = 5)
    
    utils.visualize_parameter_distr(personality_spread, personality_xmax, 'personality_score', 'simmetric_beta')

with col3:
    # ************************************************************************
    # st.subheader('Sociability Margins')
    utils.write_custom_subheader('Sociability Margins')

    sociability_spread = st.slider("""We add to each personality a 'margin'. 
                                Two people will converse only if their personality score +/- margin overlap.
                                We sample margins from a normal distribution. 
                                Choose its standard deviation.""",
                                    value = float(0.1),
                                    min_value = float(0.1),
                                    max_value = float(0.8),
                                    step = 0.1)

    utils.visualize_parameter_distr(sociability_spread, 3, 'sociability_margin', 'normal')

with col5:
    # ************************************************************************
    # st.subheader('Encouragement skew')
    utils.write_custom_subheader('Encouragement Skew')

    # depending on the value 1 through 10, beta a = the value and b = 10-the value
    encouragement_xmax = 10
    encouragement_skew = st.slider("""If someone already composts, how likely are they to encourage
                                other people to do the same? 
                                We model this probability via a beta distribution. 
                                Choose its skeweness, where higher values mean more 
                                likely to encourage others.""", 
                                    value = 5,
                                    min_value = 1, 
                                    max_value = encouragement_xmax)
    utils.visualize_parameter_distr(encouragement_skew, encouragement_xmax, 'probability_of_encouragement', 'beta')
    # ************************************************************************

with col7:
    # ************************************************************************    
    # st.subheader('Openness Skew')
    utils.write_custom_subheader('Openness Skew')
    openness_xmax = 10
    openness_skew = st.slider("""If someone doesn't compost, how likely are they to be convinced by a 
                                neighbor to start? We model this probability via a beta distribution.
                                Choose its skeweness, where higher values mean more likely to be convinced.""", 
                                    value = 3,
                                    min_value = 1, 
                                    max_value = openness_xmax)
    utils.visualize_parameter_distr(openness_skew, openness_xmax, 'probability_of_being_convinced', 'beta')

model = Interact(n_neighbors = neighborhood_size, 
                n_already_composting = num_composters,
                personality_spread = personality_spread,
                personality_xmax = personality_xmax, 
                sociability_spread = sociability_spread,
                encouragement_skew = encouragement_skew, 
                encouragement_xmax = encouragement_xmax,
                openness_skew = openness_skew, 
                openness_xmax = openness_xmax,                             
                days = 30, 
                seed = optional_seed)

# run themodel
for thick_i in range(model.ticks):
    model.step()

# collect the data
model_data = model.datacollector.get_model_vars_dataframe().reset_index()

# show day number rather than tick number
model_data['day'] = model_data['index'].divide(model_data['neighborhood_size'])  

# ************************************************************************    
st.subheader('number_of_composters over time')

my_cols_tuple = (1, 1)
col1, col2 = st.columns(my_cols_tuple)

with col1:
    utils.plot_composters_over_time(model_data, neighborhood_size)

with col2:
    # st.button('Collect data', on_click = utils.retain_model_data(model_data))
    
    st.download_button('Download collected data', data = model_data.to_csv())
    st.write(f"Data frame dimensions = {model_data.shape}")
    st.write(f"")

    # st.button('I want to reset the data before downloading them!', on_click = utils.allow_reset())

    # if st.session_state['allow_data_reset']:
    #     st.button('Reset data collection', on_click = utils.remove_model_data())
    #     st.write(f"Data frame dimensions = {st.session_state['model_data_frame'].shape}")

    st.write("""Note: the exported data is indexed by neighbors per day, 
            meaning if there are 30 people in the neighborhood, 
            there will be 30*30 = 900 rows in the data set per simulation. 
            This is because each neighbor gets a chance to interact with another 
            neighbor in a day before the day resets. You can easily modify 
            this dataset to show just the total number_of_composters at the end 
            of each day.""")
