import streamlit as st
import pandas as pd
from scipy.stats import norm, beta
import numpy as np
import altair as alt



def check_random_seed_content(random_seed):
    """This function reads in the random seed, it converts it to
    an integer if it is a number, or it leaves it as an empty string otherwise

    Args:
        random_seed (integer or ''): random seed content

    Returns:
        cleaned up random_seed (integer or '')
    """
    try:
        return int(random_seed)
    except:        
        return ''

def visualize_personality_spread_distr(personality_spread, xmax):
    """This function creates a visual of the manipulated beta distribution pdf.
    The parameters a and b of the beta distribution are related to the personality spread so that, 
    for personalities on a scale from 1 to 10
    - if personality_spread is 1, then a = b = 10
    - if personality_spread is 10, then a = b = 1

    Args:
        personality_spread (int): distribution spread
        xmax (int): max value of the slider
    """
    
    distr_df = pd.DataFrame([(x*xmax, beta.pdf(x, a = (xmax + 1) - personality_spread, b = (xmax + 1) - personality_spread)) 
                            for x in np.arange(0, 1, 0.001)], 
                            columns = ['personality_score', 'probability_density'])
    # normalization = distr_df['probability_density'].sum()
    # distr_df['probability_density'] = distr_df['probability_density']/normalization

    distr_plot = alt.Chart(distr_df).mark_area().encode(x = 'personality_score', 
                                                        y = alt.Y('probability_density', axis = alt.Axis(labels = False)))

    st.altair_chart(distr_plot)


def visualize_sociability_spread_distr(sociability_spread):
    """This function creates a visual of an asymmetric normal
    distribution centered at 0.

    Args:
        sociability_spread (float): standard deviation of the distribution

    """
    xmax = 4
    distr_df = pd.DataFrame([(x, norm.pdf(x, 0, sociability_spread)) 
                            for x in np.arange(0, xmax, 0.001)], 
                            columns = ['sociability_margin', 'probability_density'])

    distr_plot = alt.Chart(distr_df).mark_area().encode(x = 'sociability_margin',
                                                        y = alt.Y('probability_density', axis = alt.Axis(labels = False)))
    st.altair_chart(distr_plot)
    
def visualize_encourage_or_stubborn_skew_distr(skew_amount, xmax, which_one):
    """This function creates a visual of the beta distribution.
    If a<1 and b<1, the probability density function has a U shape. 
    Instead, the PDF of a beta distribution is ~ normal if a+b is 
    large enough and a~b.
    To obtain a bell curve we increase a and b artificially by changing the scale.

    Args:
        skew_amount (int): level of skewness of the distribution
        xmax (int): max value of the slider
        
    """
    if which_one == 'encouragement':
        col_name = 'probability_of_encouragement'
    elif which_one == 'stubborness': 
        col_name = 'probability_of_being_convinced'
        
    distr_df = pd.DataFrame([[x, beta.pdf(x, a = skew_amount, b = (xmax+1) - skew_amount)]
                            for x in np.arange(0, 1, 0.001)], 
                            columns = [col_name, 'probability_density'])
    distr_plot = alt.Chart(distr_df).mark_area().encode(x = col_name,
                                                        y = alt.Y('probability_density', axis = alt.Axis(labels = False)))
    st.altair_chart(distr_plot)
