
ABOUT_THE_SIMULATION = {
    'Goal': [
        """This simulation uses a condorcet method to determine the winner of a guacamole contest. 
        The goal is to show that, under some conditions, the winner you would get if you had every voter trying all guacs is
        the same as the winner you would get if you had voters sampling only a random subset.""", 
        """Limiting how many entries each voter has to taste could create opportunities around:""", 
        "- Every entrant having a fairer shot at winning, expecially the less famous ones.", 
        "- Mitigating natural behaviors, such as, the fuller you get and the lower score you might assign.", 
        "- Extending the competition to more entrants.", 
        "- ...?"
    ], 
    'Sim Setup': [
        """In this simulation you'll be able to play with how the different guacs compare to one another and the voters' preferences.
        Specifically, you'll be able to choose between 3 different guacamole configurations, and between 
        neutral voters and/or voters who like/dislike guacamole and thus tend to score higher/lower."""        
    ], 
    'Guac Config': [
        """Let's start by selecting one of the configurations below. Throughout the simulation, we'll refer to the scores in the figure as the 'true score' (TS).
        Shown in green is the guacamole with the highest TS. We'll refer to this guacamole as the true winner."""
        
    ], 
    'How Voting Works': [
        """We simulate different voters' preferences as follows. For neutral voters, votes are sampled from a normal distribution centered at TS. 
        For voters who like/dislike guacamole, votes are sampled from a normal distribution centered at TS+2 for voters who like and TS-2 for voters who dislike.
        For all voters we assume a standard deviation of 2.""", 
        """Finally, we assume that, as voters get full, they'll start assigning lower scores. 
        This is addressed via a fullness factor that is further subtracted from TS. 
        This factor decreases from 0 (when tasting begins) to -2 (when tasting ends).""", 
        "Note that all these choices are purely illustrative and are meant to give you an idea for the variety of effects you could include."
        ],

    'Let The Story Begin': [
        "But enough with the setup. Let the story begin."
        ]
    }


STORY = {
    "Introduction":  [
        """Welcome to the town of Sunnyvale, whose citizens are obsessed with all things avocado.
         While everyone agrees that guacamole is the best use of their beloved avocado, no one can agree whose guacamole recipe is the best.""",
        """The town mayor suggests to have a contest to settle once and for all on who can make the best guac. 
        The town will gather, try each one, and vote for the best!""",
        """On the day of the competition the whole town shows up to participate in tasting and voting. The entrants, 
        twenty people with big bowls of their family’s pride and joy, gather in the center of the plaza.""",
    ],

    "simulation_1": [
        """
        In this scenario our voters are asked to vote on each guacamole. 
        These will be shuffled before being randomly assigned to each person. The winning guacamole will be the one with the highest score. """, 
        """Select the percentages of voters preferences below.
        The remaining percentage will be assigned to neutral voters."""
    ], 
    "simulation_1_conclusion": [
        """Assuming there's a true winner, this can be determined even when voter’s preferences are at extreme 
        ends of the spectrum and despite how full they are (try changing the numbers and re-running the simulation).
        This is likely due to a combination of factors, including but not limited to 
        shuffling the guacamoles before randomly assigning them to each voter, 
        the standard deviation chosen, 
        the number of voters, 
        and the number of entrants.""", 
        """ Below we explore how standard deviation (std) and voters preferences affect the recovery of
        the true winner for the 'A Lot Of Contenders' configuration. This is the 
        configuration where the true winner is less likely to be recovered."""
    ], 
    "simulation_1_deep_dive": [
        """Each panel above shows the percentage of time the true winner is recovered (teal)
        or not (orange) for 100 simulations, for different percentages of people who dislike guacamole (from 0% to 50%). 
        We consider std ranging from 2 to 4 (left to right) 
        and percentages of people who like guacs (pct_ppl_like) from 0% to 50% (top to bottom). 
        As std increases (left to right), the fraction of time
        the true winner is recovered decreases (the teal region decreases in size). 
        Varying the percentages of the different voters' preferences doesn't seem to have that big of an effect.
        """
    ], 
    "simulation_2": [
        """In this scenario voters are asked to vote on a subset of guacamoles. 
        As before, these will be shuffled before being randomly assigned to each person. 
        The winning guacamole will be determined with a condorcet method (more appropriate for such configuration) 
        as the one who wins a majority of the votes in every head-to-head election 
        against each of the other entrants (a candidate preferred by more voters than any others, if it exists).""", 
        """Select the percentages of voters preferences below (the remaining percentage will be assigned to neutral voters), 
        together with the number of guacamole you'd like to assign to each voter."""
    ], 
    "simulation_2_conclusion": [
        """While you might have gotten the true winner right away, providing voters only a subset of guacamoles makes the recovery of the true
        winner a bit more difficult, expecially as the number of guacamoles for each voter is reduced. 
        You can test this by changing the numbers and re-running the simulation yourself. 
        Every time you press 'Simulate' guacamoles are randomly shuffled and the numbers can change.""", 
        """Below, we explore how standard deviation (std) and number of voters affect the recovery
        of the true winner for the 'A Lot of Contenders' configuration, the one where the true winner is less
         likely to be recovered."""
    ], 
    "simulation_2_deep_dive": [
        """As before, each panel shows the percentage of time the true winner is recovered (teal)
        or not (orange) for 200 simulations. 
        For simplicity, each voter preference accounts for about 1/3 of voters. 
        We consider std ranging from 2 to 4 (left to right) and number of voters from 100 to 300 (top to bottom). 
        As before, increasing std (left to right) decreases the fraction of time
        the true winner is recovered. Instead, increasing the number of voters has the opposite effect, 
        as it increases the fraction of time the true winner is recovered.
        """
    ], 
    "Conclusions": [
        """Whether we’re assessing which movie should take home 
        the academy award or which coworker makes the best chili, 
        these simulated contests show that we don’t need every voters in our contest 
        to assess every single entry for the competition to have a fair outcome. 
        Limiting how many entries each voter gets to assess creates an opportunity 
        to invite more entrants into the contest and allows each voter 
        to be more discerning than they perhaps could be otherwise. 
        """
    ]


}