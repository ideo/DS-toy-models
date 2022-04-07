
ABOUT_THE_SIMULATION = {
    'Goal': [
        """This simulation uses a condorcet method to determine the winner of a guacamole contest. 
        The goal is to show that the winner nominated by having each voter tasting each guacamole can be recovered even when 
        voters are assigned only a subset of contenders.""", 
        """Limiting how many entries each voter has to taste could create opportunities around:""", 
        "- Every contestant having a fairer shot at winning, expecially the less famous ones.", 
        "- Mitigating natural behaviors, such as, the fuller you get and the less excited you are to eat more (and the worse your vote is going to get).", 
        "- Extending the competition to more contestants.", 
        "- ...?"
    ], 
    'Sim Setup': [
        """In this simulation you'll be able to play with how the different guacs compare to one another and the voters' characters.
        Specifically, you'll be able to choose between 3 different guacamole configurations, and between 
        neutral voters and/or voters who really like/dislike guacamole and thus tend to upvote/downvote."""        
    ], 
    'Guac Config': [
        """Let's start by selecting one of the configurations below. Throughout the simulation, we'll refer to the scores in the figure as the 'true score' (TS).
        In green is the guacamole with the highest TS. We'll refer to this guacamole as the true winner."""
        
    ], 
    'How Voting Works': [
        """We simulate different voters' characters as follows. For neutral voters, votes are sampled from a normal distribution centered at TS. 
        For voters who really like (dislike) guacamole, votes are sampled from a normal distribution centered at TS+2 (TS-2).
        For all voters we assume a standard deviation of 2.""", 
        """Finally, we assume that, as voters get full, they'll start downvoting. 
        This is achieved via a fullness factor that is further subtracted from TS. 
        This factor decreases from 0 (when tasting begins) to -2 (when tasting ends).""", 
        "Note that all these choices are purely illustrative and are meant to give you a flavor for the variety of effects you could include."
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
        """In this scenario townpeople (our voters) are asked to vote on each guacamole. These will be shuffled before being assigned to each person. 
        The winning guacamole will be the one with the highest score. """, 
        """Select the percentages of townpeople characters below.
        The remaining percentage will be assigned to neutral voters."""
    ], 
    "simulation_1_conclusion": [
        """Assuming there's a true winner, this can be recovered most times
        even when varying the percentages of townpeople characters to the extremes, and despite the fullness factor 
        (try changing the numbers and re-running the simulation).
        This is likely due to a combination of factors, including but not limited to 
        shuffling the guacamoles before assigning them to each voter, 
        the standard deviation chosen, 
        the number of voters, 
        the number of contestants.""", 
        """ Below, we explore the parameter space in standard deviations (std) and people characters, 
        for the configuration where we expect to loose the true winner more easily: A Lot Of Contenders."""
    ], 
    "simulation_1_deep_dive": [
        """Each panel above shows the percentage of time the true winner is recovered (teal)
        or not (orange) for 100 simulations, for different percentages of people who really dislike guacamole (from 0% to 50%). 
        We consider std ranging from 2 to 4 (left to right) 
        and a percentage of people who really like guacs (pct_ppl_like) from 0% to 50% (top to bottom). 
        As std increases (left to right), the fraction of time
        the true winner is recovered decreases (the teal region decreases). 
        Varying the percentages of the different voters' characters doesn't seem to have that big of an effect.
        """
    ], 
    "simulation_2": [
        """In this scenario townpeople are asked to vote on a subset of guacamoles. 
        As before, these will be shuffled before being assigned to each person. 
        The winning guacamole will be determined with a condorcet method as the one who wins a 
        majority of the votes in every head-to-head election 
        against each of the other candidates (a candidate preferred by more voters than any others, if it exists).""", 
        """Select the percentages of townpeople characters below (the remaining percentage will be assigned to neutral voters), 
        together with the number of guacamole you'd like to assign to each voter."""
    ], 


}