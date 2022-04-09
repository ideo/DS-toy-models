# from msilib.schema import ServiceControl
import streamlit as st
import src.logic as lg
# import pandas as pd

# from src.story import STORY
from src.simulation import Simulation
# from src.simulation_unknown_best import Simulation_unknown_best



#set page initial configuration
st.set_page_config(
    page_title="Guacamole Contest",
    page_icon="img/avocado-emoji.png",
    initial_sidebar_state="collapsed")

# lg.initialize_session_state()

#extract sidebar parameters
num_townspeople, st_dev, num_guacs = lg.sidebar()

#write the title
st.title("The Allegory of the Avocados")
st.subheader("1. The Goal of This Simulation")
lg.write_about_simulation("Goal")

#write a paragraph
st.subheader("2. Simulation Setup")
lg.write_about_simulation("Sim Setup")

#write instructions for a selection tool
lg.write_custom_subsubheader("Guacamoles Configuration")
lg.write_about_simulation("Guac Config")
guac_df, scenario = lg.choose_scenario(num_guacs, ['A Lot of Contenders', 'A Close Call', 'One Clear Winner'])

lg.write_custom_subsubheader("Voters Preferences")
lg.write_about_simulation("How Voting Works")
# lg.write_about_simulation("Let The Story Begin")


#write a paragraph
st.subheader("3. Welcome to Sunnyvale")
lg.write_story("Introduction")

#adding new subsection
lg.write_custom_subheader("3.1. Scenario 1 - Tasting and Voting for All")
# st.subheader("2.1. Scenario1: Tasting and Voting for All")

section_title = "simulation_1"
lg.write_story(section_title)

pct_ppl_really_like, pct_ppl_really_dislike, dummy = lg.voters_types_and_num_guacs(section_title)

#First simulation, everyone gets everything
sim1 = Simulation(guac_df, num_townspeople, st_dev, 
                pct_ppl_really_like=pct_ppl_really_like, 
                pct_ppl_really_dislike=pct_ppl_really_dislike, 
                fullness_factor=True)
sim1.simulate(winner_metric='sum')

st.markdown("---")

#add a session state, to have the text continuing 
#after the user has interacted with this part of the simulation
if section_title not in st.session_state.keys():
    st.session_state[section_title] = False


lg.show_winner(sim1, section_title)

if st.session_state[section_title]:
    #write the conclusion
    lg.write_story('simulation_1_conclusion')
    lg.write_custom_subsubheader("A Lot Of Contenders Deep Dive")

    st.image(f"images/param_space_scan_totalSim100_a-lot-of-contenders_sum_viz.png")
    lg.write_story('simulation_1_deep_dive')
    
    
    #moving to the simulation where only a subset of guacamoles is assigned to each voter.
    lg.write_custom_subheader("3.2. Scenario 2 - Tasting and Voting for a Subset")
    # st.subheader("2.2. Scenario2: Tasting and Voting for a Subset")

    section_title = "simulation_2"
    lg.write_story(section_title)

    pct_ppl_really_like, pct_ppl_really_dislike, num_guacs_per_voter = lg.voters_types_and_num_guacs(section_title, guac_counts = True)

    sim2 = Simulation(guac_df, num_townspeople, st_dev, 
                pct_ppl_really_like=pct_ppl_really_like, 
                pct_ppl_really_dislike=pct_ppl_really_dislike, 
                num_guacs_per_voter=num_guacs_per_voter, 
                fullness_factor=True)
    sim2.simulate(winner_metric='condorcet')

    if section_title not in st.session_state.keys():
        st.session_state[section_title] = False

    lg.show_winner(sim2, section_title)
    if st.session_state[section_title]:

        #write the conclusion
        lg.write_story('simulation_2_conclusion')
        # lg.write_custom_subsubheader("A Lot Of Contenders Deep Dive")

        lg.write_custom_subsubheader("A Lot Of Contenders Deep Dive")

        st.image(f"images/param_space_scan_guacs_subset_totalSim200_townpeople100-200-300_a-lot-of-contenders_condorcet_20200408_viz.png")
        lg.write_story('simulation_2_deep_dive')

        st.subheader("4. Conclusions")

        lg.write_story('Conclusions')


# st.subheader("3. Conclusions")
# st.markdown("---")
