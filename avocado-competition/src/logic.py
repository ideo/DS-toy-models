import streamlit as st
from .guacamoles import Guacamoles

from .written_content import STORY, ABOUT_THE_SIMULATION

COLORS = {
    "blue":     "#4c78a8",
    "green":    "#9EA856",
    "red":      "#E0665C",
}

def write_about_simulation(section_title):
    """This function adds a piece of ABOUT_THE_SIMULATION 
    from written_content to the page

    Args:
        section_title (string): title of the section
    """
    for paragraph in ABOUT_THE_SIMULATION[section_title]:
        st.write(paragraph)

def write_story(section_title):
    """This function adds a piece of STORY 
    from written_content to the page

    Args:
        section_title (string): title of the section
    """
    for paragraph in STORY[section_title]:
        st.write(paragraph)

def sidebar():
    """This function contains all sidebar controls
    """
    st.sidebar.subheader("Simulation Parameters")
    
    keep_out = """
        In case you REALLY want to play more with the numbers....
    """
    st.sidebar.write(keep_out)
    
    num_townspeople = st.sidebar.slider("How many townspeople are there?", 
        value=200, 
        min_value=10, 
        max_value=500,
        step=10)
    st_dev = st.sidebar.number_input("What is the st. dev. of their randomly generated scores?",
        value=2.0,
        min_value=0.1,
        max_value=5.0,
        step=0.1
        )
    num_guacs = st.sidebar.number_input("How many guacs are in the competition?",
        value=20,
        min_value=15,
        max_value=30,
        step=1
        )
    return num_townspeople, st_dev, num_guacs


def choose_scenario(num_guacs, scenarios):
    """ This function allows the user selects a scenario, 
    which determines the 'objective score' to be used in the simulation.

    Args:
        num_guacs (int): number of guacamoles for the simulation
        scenarios (string): configuration for the simulation

    Returns:
        dataframe with objective scores
        chosen scenario
    """
    #define the structure of the entry as 2 columns
    col1, col2 = st.columns([2,5])

    #create selection list on left
    scenario = col1.radio(
        "Choose an example configuration", 
        options=scenarios,
        )

    #create guac sample based on selection
    guacs = Guacamoles(num_guacs, scenario)
    guacs_df = guacs.df

    #identify the winner
    winner = guacs_df["objective_score"].idxmax()

    #add coloring to make the winner pop up
    guacs_df["color"] = guacs_df["id"].apply(
        lambda x: COLORS["green"] if x==winner else COLORS["blue"])
    
    # # st.write(df)
    #draw the chart
    spec = {
        "height":   275,
        "mark": {"type": "bar"},
        "encoding": {
            "x":    {
                "field": "id", "type": "nominal", "sort": "id", 
                "axis": {"labelAngle": 45}
                },
            "y":    {"field": "objective_score", "type": "quantitative"},
            "color":    {"field": "color", "type": "nominal", "scale": None}
        },
        "title":    {
            "text": scenario, 
            "subtitle": f"The Best Guac is Guac No. {winner}"},   
    }

    col2.vega_lite_chart(guacs_df, spec)
    return guacs_df, scenario


def voters_types_and_num_guacs(key, guac_counts=False):
    """ This function allows the user to select voters preferences and 
    number of guacs to assign each voter.
    """
    col1, col2 = st.columns(2)
    num_guacs_per_voter = 0

    if guac_counts:
        col1, col2, col3 = st.columns(3)
    

    pct_ppl_really_like = col1.slider(
        """
        Select the % of voters who like guacamole
        """,
        value=30,
        min_value=0,
        max_value=50,
        format="%g%%",
        key=key+"ppl_really_like")

    pct_ppl_really_dislike = col2.slider(
        """
        Select the % of voters who dislike guacamole
        """,
        value=30,
        min_value=0,
        max_value=50,
        format="%g%%",
        key=key+"ppl_really_dislike")

    if guac_counts:
        num_guacs_per_voter = col3.slider(
            """
            Select the number of guacamoles for each voter
            """,
            value=10,
            min_value=0,
            max_value=20,
            key=key+"number_guacs_per_voter")

    return pct_ppl_really_like, pct_ppl_really_dislike, num_guacs_per_voter

def write_custom_subheader(text):
    """This function writes a custom sub-header

    Args:
        text (string): text to write
    """
    custom_title = '<p style="font-size: 24px; font-weight: bold">'+text+'</p>'
    st.markdown(custom_title, unsafe_allow_html=True)
    
def write_custom_subsubheader(text):
    """This function writes a custom sub-sub-header

    Args:
        text (string): text to write
    """
    custom_title = '<p style="font-size: 18px; font-weight: bold">'+text+'</p>'
    st.markdown(custom_title, unsafe_allow_html=True)    

def show_winner(sim, section_title):
    """This function shows the winning guacamole, together
    with the true winner

    Args:
        sim (simulation object)
        section_title (string): title of the section

    Returns:
        streamlit button
    """
    col1, col2, col3 = st.columns(3)

    #Creating a button to start the simulation
    start_btn = col1.button("Simulate", key='button'+section_title)
    
    #adding some space between the simulate button and the output
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns(3)

    #Showing output once the simulation is ran
    if start_btn:        
        col1.image(f"images/guac_icon_0.png", width=100)
        col2.metric(f"The winner is: ", sim.winner)
        col3.metric(f"The true winner is: ", sim.true_winner)
        
        st.session_state[section_title] = True

    return start_btn
