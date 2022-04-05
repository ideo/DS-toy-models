# from msilib.schema import ServiceControl
import streamlit as st
import src.logic as lg
# import pandas as pd

# from src.story import STORY
from src.simulation import Simulation
# from src.simulation_unknown_best import Simulation_unknown_best
# from src.tuning import tune_simulation, wrap_my_head_around_it


# wrap_my_head_around_it()

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
lg.write_about_simulation("Goal")

#write a paragraph
st.subheader("Simulation Setup")
lg.write_about_simulation("True Score")

#write instructions for a selection tool
guac_df, scenario = lg.choose_scenario(num_guacs, ['One Clear Winner', 'A Close Call', 'A Lot of Contenders'])

lg.write_about_simulation("How Voting Works")
lg.write_about_simulation("Let The Story Begin")


#write a paragraph
st.subheader("Welcome to Sunnyvale")
lg.write_story("Introduction")



st.markdown("---")
st.subheader("Time to Taste and Vote!")
section_title = "simulation_1"
lg.write_story(section_title)
# lg.write_instructions(section_title)
sim1 = Simulation(guac_df, num_townspeople, st_dev, fullness_factor=True)
sim1.simulate(winner_metric='condorcet')

# import pdb;pdb.set_trace()

# lg.animate_results(sim1, key=section_title)
# if st.session_state[f"{section_title}_keep_chart_visible"]:
#     lg.success_message(section_title, sim1.sum_success)


# st.markdown("---")
# lg.write_story("transition_1_to_2")
# st.subheader("Not Enough Guac to Go Around")
# section_title = "simulation_2"
# lg.write_story(section_title)

# col1, col2 = st.columns(2)
# lg.write_instructions(section_title, col1)
# guac_limit2 = col2.slider(
#     "How many guacs will tasters try? Start by just removing a couple and then push it from there.",
#     value=18, 
#     min_value=1, 
#     max_value=20)

# sim2 = Simulation(guac_df, num_townspeople, st_dev, assigned_guacs=guac_limit2)
# sim2.simulate()

# lg.animate_results(sim2, key=section_title)
# if st.session_state[f"{section_title}_keep_chart_visible"]:
#     lg.success_message(section_title, sim2.sum_success, guac_limit2)

# st.write("")
# st.write("")
# lg.write_story("simulation_2_a")
# lg.animate_results_of_100_runs(sim2, scenario, section_title)


# st.markdown("---")
# lg.write_story("transition_2_to_3")
# st.subheader("Different People, Different Tastes")
# section_title = "simulation_3"
# lg.write_story(section_title)
# st.text("")
# lg.write_instructions(section_title+"_a")
# pepe, fra, carlos = lg.types_of_voters(section_title)
# col1, col2 = st.columns(2)
# lg.write_instructions(section_title+"_b", col1)
# guac_limit3 = col2.slider(
#     "How many guacamoles does each voter get to try?",
#     value=15, 
#     min_value=1, 
#     max_value=20,
#     key=section_title)

# sim3 = Simulation(guac_df, num_townspeople, st_dev, 
#     assigned_guacs=guac_limit3,
#     perc_fra=fra,
#     perc_pepe=pepe,
#     perc_carlos=carlos)
# sim3.simulate()
# lg.animate_results(sim3, key=section_title)
# lg.success_message(section_title, sim3.sum_success)

# num_cronies = sum(townie.carlos_crony for townie in sim3.townspeople)
# num_effective_cronies = sum(townie.voted_for_our_boy for townie in sim3.townspeople)
# # st.caption(f"Tallying the votes by just adding them all up was a {'success' if sim3.sum_success else 'failure'}!")
# # st.caption(f"Tallying the votes using the condorcet method was a {'success' if sim3.sum_success else 'failure'}!")
# st.caption(f"{num_cronies} of Carlos's cronies voted in the contest and {num_effective_cronies} were able to vote for him.")


# st.markdown("---")
# st.subheader("A New Idea")
# section_title = "condorcet"
# lg.write_story(section_title + "_1")
# st.image("img/napkin_ballot.jpg", width=400)
# lg.write_story(section_title + "_2")

# st.text("")
# st.text("")
# # lg.write_instructions(section_title+"_1")
# pepe_4, fra_4, carlos_4 = lg.types_of_voters(section_title)
# col1, col2 = st.columns(2)
# lg.write_instructions(section_title+"_1", col1)
# guac_limit4 = col2.slider(
#     "How many guacamoles does each voter get to try?",
#     value=guac_limit3, 
#     min_value=1, 
#     max_value=20,
#     key=section_title)

# sim4 = Simulation(guac_df, num_townspeople, st_dev, 
#     assigned_guacs=guac_limit4,
#     perc_fra=fra,
#     perc_pepe=pepe,
#     perc_carlos=carlos)
# sim4.simulate()
# lg.animate_condorcet_simulation(sim4, key=section_title)
# lg.success_message(section_title, sim4.condo_success)


# st.markdown("---")
# st.subheader("Conclusion")
# st.write("Let's say something smart here.")


# st.markdown("---")
# st.subheader("Sandbox")
# st.write(
#     "If there's not yet a `sim` incorporating everything, we'll put it here!"
#     )