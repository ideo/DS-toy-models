import streamlit as st
import altair as alt
import sim_setup as setup
import numpy as np
import pandas as pd
from scipy.stats import norm, beta

st.set_page_config(layout = 'wide')

def retain_num_composters():
    # the value of the number of initial composters slider resets every time the neighborhood size changes under 50.
    # so, on each change of the neighborhood size slider, we need to save that number and put it back into the value
    # of the slider to prevent the reset
    st.session_state.n_composters = num_composters

def retain_model_data():  # saves model data to an accumulating data frame each time the collect button is pressed
    st.session_state.model_data_frame = st.session_state.model_data_frame.append(model_data)

def remove_model_data():  # resets manual data collection to empty data frame
    st.session_state.model_data_frame = pd.DataFrame()

st.header('How quickly can a neighborhood adopt the practice of composting their food scraps?')
st.write("People like to pat themselves on the back when they start doing something eco-friendly like composting,"
         "but how impactful is an isolated individual partaking in a positive behvior vs. a social individual spreading"
         "the positive behavior through their network? Tinker with the parameters representing neighbors' willingness "
         "to encourage others to compost, and their willingness to try composting if encouraged, to see how close the"
         "neighborhood gets to completely converting to composting within a 30-day period. Several neighbors are"
         "already composting at the start of each simulation. Each day, neighbors randomly meet other neighbors and"
         " decide to pair up and chat if their personalities are compatible. What conditions are necessary for "
         "composting to really take off in the neighborhood?")
col1, col2 = st.columns(2)

model_plot = None

if 'model_data_frame' not in st.session_state:
    st.session_state.model_data_frame = pd.DataFrame()

with col1:

    optional_seed = None  # unless changed, don't use random seed
    seed_input = st.text_input("Input an optional random seed. If you don't want to use a random seed, leave it blank.",
                               key = 'seed_input')
    # if seed_input == '':  # if input empty string, don't use a seed
    #     optional_seed = None

    try:  # if input is text, throw an error
        if seed_input == '':  # if input empty string, don't use a seed
            optional_seed = None
        elif int(float(seed_input)) != float(seed_input):  # if it's numeric but not an integer, throw error
            # this will throw an error if the input is not numeric as well
            raise Exception('Random seed must be an integer!')
        else:
            optional_seed = int(float(seed_input))  # if everything fine, set the seed as the input

        # once the seed is accepted:

        # TODO: be able to select number of days

        st.subheader('Neighborhood size')
        neighborhood_size = st.slider('How many people live in the neighborhood?', min_value = 10, max_value = 200, step = 10,
                                      value = 70,
                                      key = 'nbhd',
                                      on_change = retain_num_composters)  # saves the state of num_composters on each change

        st.subheader('Number of initial composters')
        num_composters = st.slider('How many people are randomly chosen to be composters at the beginning of the simulation?',
                                   min_value = 1, max_value = int(min(50, neighborhood_size)/2), value = 5,
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

    except Exception as e:
        st.write(e)
        st.write('Random seed must be an integer!')  # TODO: it threw an exception after manipulating a few of the sliders but i can't replicate it. wasn't related to seed

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

