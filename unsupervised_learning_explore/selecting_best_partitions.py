import numpy as np
import pandas as pd
import random

class selection_process(object):

    def __init__(self, explore_df, list_models, decision_quartile, point_criterion):

        self.explore_df = explore_df
        self.list_models = list_models
        self.decision_quartile = decision_quartile
        self.point_criterion = point_criterion
        self.selected_partitions = None

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

        low_value = q1_value - (self.decision_quartile * interquartil)
        high_value = q3_value + (self.decision_quartile * interquartil)

        return [low_value, high_value]

    def __estimated_z_score(self, list_value):

        z_score_positive = np.mean(list_value) + (np.std(list_value) * self.point_criterion)
        z_score_negative = np.mean(list_value) - (np.std(list_value) * self.point_criterion)
        return [z_score_negative, z_score_positive]

    def __make_positive_selection(self, z_score, q_value, list_values):
        select_examples = []

        for i in range(len(self.explore_df)):
            row_response = []

            if list_values[i] >= q_value:
                row_response.append(1)
            else:
                row_response.append(0)

            if list_values[i] >= z_score:
                row_response.append(1)
            else:
                row_response.append(0)

            select_examples.append(sum(row_response))
        return select_examples

    def __make_negative_selection(self, z_score, q_value, list_values):
        select_examples = []

        for i in range(len(self.explore_df)):
            row_response = []

            if list_values[i] <= q_value:
                row_response.append(1)
            else:
                row_response.append(0)

            if list_values[i] <= z_score:
                row_response.append(1)
            else:
                row_response.append(0)

            select_examples.append(sum(row_response))
        return select_examples

    def select_best_calinski_siluetas(self, performance):

        quartiles_values = self.__estimated_interquartile(self.explore_df[performance])
        z_score = self.__estimated_z_score(self.explore_df[performance])
        self.explore_df["selected_{}".format(performance)] = self.__make_positive_selection(z_score[1],
                                                                                            quartiles_values[1],
                                                                                            self.explore_df[
                                                                                                performance])

    def select_best_davis(self, performance):

        quartiles_values = self.__estimated_interquartile(self.explore_df[performance])
        z_score = self.__estimated_z_score(self.explore_df[performance])
        self.explore_df["selected_{}".format(performance)] = self.__make_negative_selection(z_score[0],
                                                                                            quartiles_values[0],
                                                                                            self.explore_df[
                                                                                                performance])

    def __update_decision(self, performance_name, criterion, value):

        list_values = []
        for i in range(len(self.explore_df)):
            if criterion == 1:  # higher
                if self.explore_df[performance_name][i] >= value:
                    list_values.append(3)
                else:
                    list_values.append(0)
            else:  # lower
                if self.explore_df[performance_name][i] <= value:
                    list_values.append(3)
                else:
                    list_values.append(0)
        # updating
        self.explore_df["selected_{}".format(performance_name)] = list_values

    def evaluate_selection_process(self, performance_list):

        for performance in performance_list:
            key = "selected_{}".format(performance)
            df_summary = self.explore_df.loc[self.explore_df[key] > 0]
            if len(df_summary) <= 0:
                print("Updating performances")
                if "cal" in performance or "sil" in performance:
                    max_value = np.max(self.explore_df[performance])
                    self.__update_decision(performance, 1, max_value)
                else:
                    min_value = np.min(self.explore_df[performance])
                    self.__update_decision(performance, 0, min_value)

    def __create_index_account(self, list_index):

        index_values = []
        for indexes in list_index:
            values = [index for index in indexes]
            index_values+=values

        index_values = list(set(index_values))
        return index_values

    def select_partitions_by_performances(self, performance_list, path_export):

        index_list = []
        for performance in performance_list:
            key = "selected_{}".format(performance)
            df_selected = self.explore_df.loc[self.explore_df[key] != 0]
            index_list.append(df_selected.index)

        index_to_process = self.__create_index_account(index_list)

        matrix_data = []

        for index in index_to_process:
            row = [self.explore_df[key][index] for key in self.explore_df.columns]
            matrix_data.append(row)

        self.selected_partitions = pd.DataFrame(matrix_data, columns=self.explore_df.columns)
        try:
            self.selected_partitions.drop(columns=['Unnamed: 0'], inplace=True)
        except:
            pass

        print("Exporting select partitions")
        name_export = "{}selected_partition_process_{}.csv".format(path_export, random.randint(1, 100)*100)
        print(name_export)
        self.selected_partitions.to_csv(name_export, index=False)