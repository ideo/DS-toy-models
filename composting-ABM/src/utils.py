import streamlit as st

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

def retain_num_composters(num_composters):
    """This function stores the initial number of composters selected every time
    the Neighborhood size slider is changed. 
    This has to occur
    """
    # the value of the number of initial composters slider 
    # resets every time the neighborhood size changes under 50.
    # so, on each change of the neighborhood size slider, 
    # we need to save that number and put it back into the value
    # of the slider to prevent the reset
    st.session_state["n_composters"] = num_composters
