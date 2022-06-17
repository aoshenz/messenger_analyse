import utils as utils
class Messenger:

    def __init__(self):
        pass

    def analyse(self):
        # run all the other functions here

    def time_of_day(self):
        pass

        # some attributes to show plot
        # e.g. self.time_of_day_plot = time_of_day_plot
    
    def load_all_data(self):

        df = utils.import_data(create_new_file=False, limit_files=None)


        self.all_data = df

        return df
    

# Steps
# 1. load data
# 2. analyse (which runs all the other functions)
# 3. render
