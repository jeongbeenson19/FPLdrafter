import pandas as pd


class DataFramePreprocessor:

    def __init__(self):
        with open("fpl-data-stats.csv") as self.data:
            self.data = pd.read_csv(self.data)
            self.df = pd.DataFrame(self.data)

    def web_name_list_maker(self, n) -> int:
        """
        1 for Goalkeepers, 2 for Deffenders, 3 for Midfielders, 4 for Forwards
        """
        self.df = self.df[self.df['element_type'] == n]
        self.web_name = self.df.drop_duplicates(subset=['web_name'])
        self.web_name = self.web_name['web_name']
        self.web_name = self.web_name.to_list()
        return self.web_name


def var_optimizer(self, element_type=None, value="total_points"):
    """
    DataFrame includes Goalkeepers' stat
    """
    if isinstance(element_type, int):
        df = self.df[self.df['element_type'] == element_type]
    else:
        df = self.df
    row = df.drop(columns=['id', 'element_type', 'team_name',
                           'opponent_team_name', 'was_home', 'now_cost', 'selected_by_percent', 'gameweek'])
    row = row.groupby('web_name').sum()
    row = row.sort_values([value], ascending=False)
    return row
