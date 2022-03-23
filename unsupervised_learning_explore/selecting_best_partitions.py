import numpy as np
import pandas as pd
from scipy import stats

class selection_process(object):

    def __init__(self, explore_df, list_models, decision_quartile, point_criterion):

        self.explore_df = explore_df
        self.list_models = list_models
        self.decision_quartile = decision_quartile
        self.point_criterion = point_criterion

    def get_statistics_values_by_performance(self, list_metrics):

        print("Estimating statistics values")
        statistics_df = pd.DataFrame()
        statistics_df['statistics'] = ['average', 'std', 'min_value', 'max_value', 'q1_value', 'q3_value']

        for performance in list_metrics:
            mean = np.mean(self.explore_df[performance])
            std = np.std(self.explore_df[performance])
            min_value = np.min(self.explore_df[performance])
            max_value = np.max(self.explore_df[performance])
            q1_value = np.quantile(self.explore_df[performance], .25)
            q3_value = np.quantile(self.explore_df[performance], .50)

            statistics_df[performance] = [mean, std, min_value, max_value, q1_value, q3_value]

        return statistics_df

    def __estimated_interquartile(self, list_values):
        q1_value = np.quantile(list_values, .25)
        q3_value = np.quantile(list_values, .75)
        interquartil = q3_value - q1_value

        low_value = q3_value - (self.decision_quartile * interquartil)
        high_value = q3_value + (self.decision_quartile * interquartil)

        return [low_value, high_value]

    def __estimated_z_score(self, list_value):

        z_score_positive = np.mean(list_value) + (np.std(list_value) * self.point_criterion)
        z_score_negative = np.mean(list_value) - (np.std(list_value) * self.point_criterion)
        return [z_score_negative, z_score_positive]

    def __make_positive_selection(self, z_score, q_vale, list_values):
        select_examples = []

        for i in range(len(self.explore_df)):
            row_response = []

            if list_values[i] >= q_vale:
                row_response.append(1)
            else:
                row_response.append(0)

            if list_values[i] >= z_score:
                row_response.append(1)
            else:
                row_response.append(0)

            select_examples.append(sum(row_response))
        return select_examples

    def select_best_calinski_siluetas(self, performance):

        quartiles_values = self.__estimated_interquartile(self.explore_df[performance])
        z_score = self.__estimated_z_score(self.explore_df[performance])
        self.explore_df["selected_{}".format(performance)] = self.__make_positive_selection(z_score[1], quartiles_values[1], self.explore_df[performance])

    def select_best_davis(self, performance):




