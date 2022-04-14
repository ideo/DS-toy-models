import streamlit as st
import altair as alt
import sim_setup as setup
import numpy as np
import pandas as pd
from scipy.stats import norm, beta
import src.utils as utils

st.set_page_config(layout = 'wide')


def retain_model_data():  # saves model data to an accumulating data frame each time the collect button is pressed
    st.session_state.model_data_frame = st.session_state.model_data_frame.append(model_data)

def remove_model_data():  # resets manual data collection to empty data frame
    st.session_state.model_data_frame = pd.DataFrame()

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

model_plot = None

#initialize the model dataframe to an empty one if not already in the 
#session state.
if 'model_data_frame' not in st.session_state:
    st.session_state.model_data_frame = pd.DataFrame()

col1, col2 = st.columns(2)

with col1:

    #request the user an optional random seed    
    st.subheader('Random Seed')
    seed_input = st.text_input("""Input an optional integer random seed or leave it blank.""",
                               key = 'seed_input')

    # Check on random seed. Accept only numbers.
    seed_input = utils.check_random_seed_content(seed_input)
    optional_seed = seed_input if seed_input!= '' else None
    if optional_seed == None:
        st.write(f"Random seed = {optional_seed}")

    # TODO: be able to select number of days
    
    # pick the neghborhood size
    st.subheader('Neighborhood size')
    neighborhood_size = st.slider('How many people live in the neighborhood?', 
                                    min_value = 10, 
                                    max_value = 200, 
                                    step = 10,
                                    value = 70,
                                    key = 'nbhd')

    # pick the fraction of initial composters as a percentage of the neighborhood size
    st.subheader('Fraction of initial composters')
    frac_composters = st.slider('What is the % of composters at the beginning of the simulation?',
                                min_value = 1, 
                                max_value = 50, 
                                value = 10,
                                format="%g%%",
                                key = 'n_composters')
                                
    num_composters = int(frac_composters*neighborhood_size/100)
    st.write(f"({num_composters} composters)")

    st.subheader('Spread of Personalities')
    st.write(""" We create personality scores from 1 to 10 by sampling them from 
                a symmetric beta distribution and multiplying the result by 10.
                We choose this distribution because of its convenient shape
                (bounded between 0 and 1, centered at 0.5) and because it tapers off smoothly at 
                the boundaries.""")
    xmax = 10
    personality_spread = st.slider("""Choose the spread of this distribution, from narrow (1) to flat (10)""",
                                    min_value = 1, 
                                    max_value = xmax, 
                                    value = 5)
    
    utils.visualize_parameter_distr(personality_spread, xmax, 'personality_score', 'simmetric_beta')

    st.subheader('Sociability Margins')
    st.write("""We enrich each personality by adding a 'margin'. 
            This defines who people are willing to talk to. Two people will 
            only converse if their personality margins (personality score +/- margin) overlap.
            Margins are sampled from an asymmetric normal distribution centered at 0.""")
    sociability_spread = st.slider('Choose the standard deviation of this distribution.',
                                    value = float(1),
                                    min_value = float(0.5), 
                                    max_value = float(1.5), 
                                    step = 0.1)

    utils.visualize_parameter_distr(sociability_spread, 4, 'sociability_margin', 'normal')

    
    st.subheader('Encouragement skew')
    st.write("""If someone already composts, how likely are they to encourage
                other people to do the same? We model this probability via a beta distribution and you
                can choose its skeweness.""")

    # depending on the value 1 through 10, beta a = the value and b = 10-the value
    xmax = 10
    encouragement_skew = st.slider("""Choose its skeweness. Higher values mean more 
                                    likely to encourage others.""", 
                                    value = 5,
                                    min_value = 1, 
                                    max_value = xmax)
    utils.visualize_parameter_distr(encouragement_skew, xmax, 'probability_of_encouragement', 'beta')

    st.subheader('Stubbornness skew')
    st.write("""If someone doesn't compost, how likely are they to be convinced by a 
            neighbor to start? We model this probability via a beta distribution and you
            can choose its skeweness.""")
    
    xmax = 10
    stubbornness_skew = st.slider("""Choose its skeweness. Higher values mean more 
                                    likely to be convinced.""", 
                                    value = 3,
                                    min_value = 1, 
                                    max_value = 10)
    utils.visualize_parameter_distr(stubbornness_skew, xmax, 'probability_of_being_convinced', 'beta')

    model = setup.Interact(n_neighbors = neighborhood_size, n_already_composting = num_composters,
                            personality_spread = personality_spread,
                            sociability_spread = sociability_spread,
                            encouragement_beta_a = encouragement_skew, encouragement_beta_b = 11 - encouragement_skew,
                            stubbornness_beta_a = stubbornness_skew, stubbornness_beta_b = 11 - stubbornness_skew,
                            days = 30, seed = optional_seed)

    for current_tick in range(model.ticks):
        model.step()
        # print([n.compost for n in model1.neighbors])

    model_data = model.datacollector.get_model_vars_dataframe().reset_index()
    model_data['index'] = model_data['index'].divide(model_data['Neighborhood Size'])  # show day number rather than tick number

    model_plot = alt.Chart(model_data).mark_line().encode(x = alt.X('index', axis = alt.Axis(title = 'Day')),
                                                            y = 'Number of Composters').\
        encode(alt.Y('Number of Composters', scale = alt.Scale(domain = [0, neighborhood_size])))

with col2:
    # st.write(st.session_state)

    st.subheader('Number of composters over time')
    if model_plot is not None:
        st.altair_chart(model_plot, use_container_width = True)

    st.button('Collect data', on_click = retain_model_data)
    st.write('Data frame dimensions:', st.session_state.model_data_frame.shape)
    st.button('Reset data collection', on_click = remove_model_data)
    st.download_button('Download collected data', data = st.session_state.model_data_frame.to_csv())
    st.write('Note: the exported data is indexed by neighbors per day, meaning if there are 30 people in the '
             'neighborhood, there will be 30*30 = 900 rows in the data set per simulation. This is because each neighbor '
             'gets a chance to interact with another neighbor in a day before the day resets. You can easily modify '
             'this dataset to show just the total number of composters at the end of each day.')

