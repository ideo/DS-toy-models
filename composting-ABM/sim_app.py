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
    seed_input = st.text_input("""Input an optional integer random seed or leave it blank.""",
                               key = 'seed_input')

    # Check on random seed. Accept only numbers.
    seed_input = utils.check_random_seed_content(seed_input)
    optional_seed = seed_input if seed_input!= '' else None
    if optional_seed == None:
        st.write(f"Random seed = {optional_seed}")

    # TODO: be able to select number of days
    st.subheader('Neighborhood size')
    
    if 'n_composters' not in st.session_state.keys():
        initial_value_composters = 5
        num_composters = initial_value_composters

    #FIXME HERE
    neighborhood_size = st.slider('How many people live in the neighborhood?', 
                                    min_value = 10, 
                                    max_value = 200, 
                                    step = 10,
                                    value = 70,
                                    key = 'nbhd', 
                                    on_change = utils.retain_num_composters(num_composters))  # saves the state of num_composters on each change

    st.subheader('Number of initial composters')

    # The max number of initial composters is either 25 or lower (for neighbours with less than 50 ppl)
    num_composters = st.slider('How many people are randomly chosen to be composters at the beginning of the simulation?',
                                min_value = 1, 
                                max_value = int(min(50, neighborhood_size)/2), 
                                value = initial_value_composters,
                                key = 'n_composters')

    st.subheader('Spread of distribution of personality scores')
    personality_spread = st.slider('Personality scores are on a Beta(a, b) distribution. When Beta parameters A and'
                                            ' B are equal, the shape of the distribution resembles a bell curve across the '
                                            'interval 0 to 1, centered at 0.5. This spread parameter is inversely based on '
                                            'increasing both Beta parameters. Then, since personality scores are on a scale '
                                            'of 1 through 10, we multiply the randomly generated value by 10.',
                                    min_value = 1, max_value = 10, value = 5)
    personality_spread_distr = pd.DataFrame([[x*10, beta.pdf(x, a = 11 - personality_spread, b = 11 - personality_spread)]
                                                for x in np.arange(0, 1, 0.001)])  # TODO: fix y axis bounds
    personality_spread_distr.columns = ['Personality Score', 'y']
    personality_spread_plot = alt.Chart(personality_spread_distr).mark_area().encode(x = 'Personality Score',
                                                                                        y = alt.Y('y', axis = alt.Axis(title = 'Probability Density', labels = False)))
    st.altair_chart(personality_spread_plot)

    st.subheader('Standard deviation of Normal distribution of sociability margins')
    sociability_spread = st.slider('Each person in the neighborhood has a "margin" about their personality that defines'
                                    ' who they are willing to talk to. Two people will only converse if their personality'
                                    ' margins overlap',
                                    value = float(1),
                                    min_value = float(0.5), max_value = float(1.5), step = 0.1)
    sociability_spread_distr = pd.DataFrame([[x, norm.pdf(x, 0, sociability_spread)] for x in np.arange(0, 4, 0.001)])
    # recall that this is a half distribution because we take the absolute value of the score--it's a margin
    sociability_spread_distr.columns = ['Sociability Margin', 'y']
    sociability_spread_plot = alt.Chart(sociability_spread_distr).mark_area().encode(x = 'Sociability Margin',
                                                                                        y = alt.Y('y', axis = alt.Axis(title = 'Probability Density', labels = False)))
    st.altair_chart(sociability_spread_plot)

    st.subheader('Encouragement skew')
    # depending on the value 1 through 10, beta a = the value and b = 10-the value
    encouragement_skew = st.slider('If someone composts already, how likely are they to encourage others to compost?'
                                    ' A higher value means more likely.', value = 5,
                                    min_value = 1, max_value = 10)
    encouragement_skew_distr = pd.DataFrame([[x, x * 10, beta.pdf(x, a = encouragement_skew, b = 11 - encouragement_skew)]
                                                for x in np.arange(0, 1, 0.001)])
    encouragement_skew_distr.columns = ['Probability of Encouragement', 'x', 'y']
    encouragement_skew_plot = alt.Chart(encouragement_skew_distr).mark_area().encode(x = 'Probability of Encouragement',
                                                                                        y = alt.Y('y', axis = alt.Axis(title = 'Probability Density', labels = False)))
    st.altair_chart(encouragement_skew_plot)

    st.subheader('Stubbornness skew')
    # similar idea as last slider with beta distribution
    stubbornness_skew = st.slider("If someone doesn't compost, how likely are they to be convinced by a neighbor to start?"
                                    " A higher value means more likely.", value = 3,
                                    min_value = 1, max_value = 10)
    stubbornness_skew_distr = pd.DataFrame([[x, x * 10, beta.pdf(x, a = stubbornness_skew, b = 11 - stubbornness_skew)]
                                                for x in np.arange(0, 1, 0.001)])
    stubbornness_skew_distr.columns = ['Probability of Being Convinced', 'x', 'y']
    stubbornness_skew_plot = alt.Chart(stubbornness_skew_distr).mark_area().encode(x = 'Probability of Being Convinced',
                                                                                    y = alt.Y('y', axis = alt.Axis(title = 'Probability Density', labels = False)))
    st.altair_chart(stubbornness_skew_plot)

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

