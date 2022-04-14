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

def sample_from_beta_distr_pdf(x, xmax, param, simmetric):
    """This function samples from the pdf of a custom beta distribution

    Note:
    - If a<1 and b<1 -> the pdf has a U shape. 
    - If a+b is large enough and a~b -> the pdf has a bell shape.
    --> in some cases we can pick a and b to create the shape we need.

    For a simmetric beta, param == spread:
      - if spread is 1, then a = b = xmax
      - if spread is xmax, then a = b = 1
    
    For asimmetric beta, param == probability of success

    Args:
        x (int): value to sample 
        xmax (int): max value for x-axis
        spread (int): width
        simmetric (bool): whether the beta distribution is simmetric or not

    Returns:
        float: the pdf(x)
    """
    if simmetric:
        pdf = beta.pdf(x, a = (xmax + 1) - param, b = (xmax + 1) - param)
    else:
        pdf = beta.pdf(x, a = param, b = (xmax+1) - param)
    return pdf

def sample_from_normal_distr_pdf(x, mean, std):
    """This function samples from a normal distribution

    Args:
        x (float): value to sample pdf of
        mean (float): mean of the distribution
        std (float): standard deviation of the distribution

    Returns:
        float: the pdf(x)
    """
    return norm.pdf(x, mean, std)

def visualize_parameter_distr(param, xmax, param_name, distribution):
    """This function creates a visual of the spread 
    of a given parameter assuming it follows a given distribution.

    Args:
        personality_spread (int): distribution spread
        xmax (int): max value of the slider
        param_name (str): name of the parameter for viz purposed
        distribution (str): distribution to sample from
    """

    if 'beta' in distribution:
        simmetric = True if 'simmetric' in distribution else False        
        distr_df = pd.DataFrame([(x*xmax, 
                                  sample_from_beta_distr_pdf(x, xmax, param, simmetric)) 
                                for x in np.arange(0, 1, 0.001)])
    
    elif distribution == 'normal':
        distr_df = pd.DataFrame([(x*xmax, 
                                  sample_from_normal_distr_pdf(x, 0, param)) 
                                for x in np.arange(0, xmax, 0.001)])

    distr_df.columns = [param_name, 'probability_density']
    distr_plot = alt.Chart(distr_df).mark_area().encode(x = param_name, 
                                                        y = alt.Y('probability_density', axis = alt.Axis(labels = False)))

    st.altair_chart(distr_plot)

    
