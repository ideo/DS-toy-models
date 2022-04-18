# Things you get exposed to with this toy model
- Streamlit
- Agent Based Modeling via the python library Mesa
- Using python classes
- Docstrings

# About this toy model
In this toy model we use Mesa to simulate the process of a positive behavior (like composting) moving through a neighborhood. Via a streamlit app, we allow the user to explore how
such propagation depends on the level of compatibility between neighbors and a the propensity of neighbors to talk about that behavior with others / adopt the behavior if encouraged to.

# How to run it
- Install the required packages from pipenv via `pipenv install`.
- Run the script via `pipenv run streamlit run sim_app.py`
- Interact with the simulation by clicking on the local URL that appears in the terminal at runtime. You can also share this simulation externally via the network URL.

# Links and Resources
### Learning Mesa
- https://towardsdatascience.com/intro-to-agent-based-modeling-3eea6a070b72 Supermarket cashier model
- https://dmnfarrell.github.io/bioinformatics/abm-mesa-python COVID infection model

### Agent-Based Modeling
- One of the most famous ABMs: the Schelling segregation model https://ncase.me/polygons/ 
- Agent-based modeling: Methods and techniques for simulating human systems https://www.pnas.org/doi/10.1073/pnas.082080899 
- Simple or complicated agent-based models? A complicated issue (doi: 10.1016/j.envsoft.2016.09.006) http://manuscript.elsevier.com/S1364815216306041/pdf/S1364815216306041.pdf

# Note: Still needs to be tested for user feedback
