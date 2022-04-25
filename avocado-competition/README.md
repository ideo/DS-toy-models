# Things you get exposed to with this toy model
- Streamlit
- Adding tests via pytest
- Using python classes 
- Docstrings

# About this toy model
This simulation uses a condorcet method to determine the winner of a guacamole contest. 
The goal is to show that, under some conditions, the winner you would get if you had every voter trying all guacs is the same as the winner you would get if you had voters sampling only a random subset. 

Limiting how many entries each voter has to taste could create opportunities around, e.g.:
- Every entrant having a fairer shot at winning, expecially the less famous ones. 
- Mitigating natural behaviors, such as, the fuller you get and the lower score you might assign. 
- Extending the competition to more entrants.

You can find a live version of this simulation [here]{https://share.streamlit.io/ideo/ds-toy-models/deploy/avocado-competition/app.py}.
# How to run it
Install the required packages from pipenv via 
`pipenv install`

Run the tests via
`pipenv run python -m pytest`

Run the script via 
`pipenv run streamlit run app.py`

Interact with the simulation by clicking on the local URL that appears in the terminal at runtime. You can also share this simulation externally via the network URL.

# About the deep dive visuals

Some of the visuals contained in the simulation have been pre-generated via the script `param_space_scan.py` and the jupyter notebook `parameter_space_visual.ipynb`.


### WARNING - Streamlit & Pandas Version Conflicts

Streamlit will let you develop locally with the latest python (3.9.x) but can only host up to python 3.7.12. The latest pandas has moved on from python 3.7. All this is to say, please don't change the python and pandas versions specified in the pipenv files.