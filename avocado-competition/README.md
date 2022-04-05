# About this toy model

This simulation uses a condorcet method to determine the winner of a guacamole contest.
The goal of this exercise is to show that to have a fair outcome we don’t need every judge in the contest to assess every contender. 
Limiting how many entries each judge gets to assess creates several opportunities, such as:
- Each contender might have a fairer shot at winning (e.g., the fuller you get and the less excited you are to eat more guac)
- More participants could be invited to the contest

This simulation uses streamlit. Given some limitations of streamlit this script uses python 3.7.

# How to run it

Install the required packages from pipenv via 
`pipenv install`

Run the tests via
`pipenv run python -m pytest`

Run the script via 
`pipenv run streamlit run app.py`

