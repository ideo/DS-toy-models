# Things you get exposed to with this toy model
- Streamlit
- Adding tests via pytest
- Using python classes 
- Docstrings

# About this toy model
This simulation uses a condorcet method to determine the winner of a guacamole contest. 
The goal is to show that the winner nominated by having each voter tasting each guacamole can be recovered even when 
voters are assigned only a subset of contenders.

Limiting how many entries each voter has to taste could create opportunities around, e.g.:
- Every contestant having a fairer shot at winning, expecially the less famous ones
- Mitigating natural behaviors, such as, the fuller you get and the less excited you are to eat more (and the worse your vote is going to get)
- Extending the competition to more contestants.

# How to run it
Install the required packages from pipenv via 
`pipenv install`

Run the tests via
`pipenv run python -m pytest`

Run the script via 
`pipenv run streamlit run app.py`


### WARNING - Streamlit & Pandas Version Conflicts

Streamlit will let you develop locally with the latest python (3.9.x) but can only host up to python 3.7.12. The latest pandas has moved on from python 3.7. All this is to say, please don't change the python and pandas versions specified in the pipenv files.