import pandas as pd

class Guacamoles():
    def __init__(self, num_guacs, scenario):

        self.num_guacs = num_guacs
        
        self.scenario = scenario.lower()
        
        self.df = self.get_guac_df()
        
    def get_guac_df(self):
        if self.scenario == 'one clear winner':
            return self.get_clear_winner()
        
        elif self.scenario == 'a lot of contenders':
            return self.get_lots_contenders()
        
        elif self.scenario == 'a close call':
            return self.get_close_call()
    
    def get_clear_winner(self):
        scores = [4, 5, 2, 7, 6, 10, 7, 4, 2, 7, 5, 2, 5, 7, 2, 5, 4, 7, 2, 4]
        return self.get_dataframe(scores)

    def get_lots_contenders(self):
        scores = [4, 5, 4, 7, 6, 8, 7, 9, 5, 8, 9.5, 8, 10, 8, 9, 5, 9, 7, 8, 4]
        return self.get_dataframe(scores)

    def get_close_call(self):
        scores = [4, 5, 2, 7, 6, 8, 7, 4, 6, 10, 9.5, 2, 5, 8, 3, 5, 4, 7, 2, 4]
        return self.get_dataframe(scores)

    def get_dataframe(self, scores):
        my_tuple = [(i, scores[i]) for i in range(self.num_guacs)] 
        return pd.DataFrame(my_tuple, columns = ['id', 'objective_score'])

