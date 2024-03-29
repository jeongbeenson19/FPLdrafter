import pandas as pd


class DataFramePreprocessor:

    def __init__(self):
        with open("fpl-data-stats.csv") as self.data:
            self.data = pd.read_csv(self.data)
            self.df = pd.DataFrame(self.data)

    def web_name_list(self, n) -> int:
        """
        Create a list of players' web names based on the specified element type.

        Args:
            n (int): Element type to filter players. 
                1 for Goalkeepers, 2 for Defenders, 3 for Midfielders, 4 for Forwards.

        Returns:
            list: A list containing unique web names of players belonging to the specified element type.

        Notes:
            Filters the DataFrame to include only players of the specified element type.
            Then, extracts unique web names and returns them as a list.
        """
        df = self.df[self.df['element_type'] == n]
        web_name = df.drop_duplicates(subset=['web_name'])
        web_name = web_name['web_name']
        web_name = web_name.to_list()
        return web_name

    def summarize_player_statistics(self, element_type=None, value="total_points"):
        """
        Summarize player statistics based on specific element type and value.

        Args:
            element_type (int, optional): Type of players to filter.
                1 for Goalkeepers, 2 for Defenders, 3 for Midfielders, 4 for Forwards.
                If not specified, includes all players. Defaults to None.
            value (str, optional): Name of the variable to be sorted by.
                Can be one of the following: 'minutes', 'shots', 'SoT', 'SiB', 'xG', 'npxG', 'G', 'npG',
                'key_passes', 'xA', 'A', 'xGC', 'GC', 'xCS', 'CS', 'xGI', 'npxGI', 'xP',
                'total_points', 'PvsxP', 'pos_touches', 'Att Pen', 'carries_final_third', 'carries_penalty_area'.
                Defaults to "total_points".

        Returns:
            pandas.DataFrame: DataFrame containing optimized player statistics.

        Notes:
            If element_type is specified, filters the DataFrame to include only players of the specified type.
            Then, removes unnecessary columns, aggregates the data by player name, and sorts the DataFrame
            based on the specified value column in descending order.
            If element_type is not specified, uses the entire DataFrame for summarization.
        """
        if isinstance(element_type, int):
            df = self.df[self.df['element_type'] == element_type]
        else:
            df = self.df
        df = df.drop(columns=['id', 'element_type', 'team_name',
                              'opponent_team_name', 'was_home', 'now_cost', 'selected_by_percent', 'gameweek'])
        df = df.groupby('web_name').sum()
        df = df.sort_values([value], ascending=False)
        df['efficiency'] = df['total_points'] / df['minutes']
        df.fillna(0, inplace=True)
        return df
