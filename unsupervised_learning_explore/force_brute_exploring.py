import classical_ml_clustering
import evaluation_cluster
import pandas as pd
import random

class exploring_clustering(object):

    def __init__(self, dataset, path_export, max_k_values, min_examples_per_group, max_examples_per_group, index_examples):
        self.dataset = dataset
        self.path_export = path_export
        self.explore_results = []
        self.max_k_values = max_k_values
        self.min_examples_per_group = min_examples_per_group
        self.max_examples_per_group = max_examples_per_group
        self.exploring_instance = classical_ml_clustering.aplicateClustering(self.dataset)
        self.eval_performances = evaluation_cluster.evaluationClustering()
        self.df_with_labels = pd.DataFrame()
        self.df_explore_to_export = None
        self.index_examples = index_examples

    def __evaluate_algorithm(self, algorithm, response, params, model_instance):

        if response == 0:
            performances = self.eval_performances.get_metrics(model_instance.dataSet,
                                                              model_instance.labels)
            if performances[0] != "ERROR" and performances[1] != "ERROR" and performances[2] != "ERROR":
                #Adding to performances metrics list
                random_data = random.randint(1, 1000)*100
                iteration = "process_{}".format(random_data)
                row = [iteration, algorithm, params, model_instance.number_groups, performances[0], performances[1], performances[2]]
                self.df_with_labels[iteration] = model_instance.labels
                self.explore_results.append(row)

    def __exploring_with_k_params(self):

        for k in range(2, self.max_k_values+1):
            response_apply = self.exploring_instance.aplicateKMeans(k)
            self.__evaluate_algorithm("KMEANS", response_apply, "k={}".format(k), self.exploring_instance)

            response_apply = self.exploring_instance.aplicateBirch(k)
            self.__evaluate_algorithm("BIRCH", response_apply, "k={}".format(k), self.exploring_instance)

    def __exploring_agglomerative_ks(self):

        for k in range(1, self.max_k_values+1):
            for linkage in ['ward', 'average']:
                for affinity in ['euclidean']:
                    params = "linkage: {}-affinity: {}-k: {}".format(linkage, affinity, k)
                    response_apply = self.exploring_instance.aplicateAlgomerativeClustering(linkage, affinity, k)
                    self.__evaluate_algorithm("Agglomerative", response_apply, params, self.exploring_instance)

    def __exploring_optics(self):

        for xi in [0, 0.01]:
            for min_size in [0, 0.01]:
                params = "min_members: {}-xi: {}-min_size: {}".format(self.min_examples_per_group, xi, min_size)
                response_apply = self.exploring_instance.applicateOptics(self.min_examples_per_group, xi, min_size)
                self.__evaluate_algorithm("OPTICS", response_apply, params, self.exploring_instance)

    def __export_results(self):
        print("Exporting results")
        random_data = random.randint(1, 10000) * 100
        self.df_explore_to_export = pd.DataFrame(self.explore_results, columns=["iteration", "algorithm", "params", "generated_groups", "calinski_haraabasz", "siluetas", "davis"])
        name_export = "exploring_result_{}.csv".format(random_data)
        print(name_export)
        self.df_explore_to_export.to_csv(self.path_export+name_export, index=False)

        name_export = "df_with_labels_{}.csv".format(random_data)
        print(name_export)
        self.df_with_labels['index_examples'] = self.index_examples
        self.df_with_labels.to_csv(self.path_export + name_export, index=False)

    def start_exploring(self):

        #DBScan
        print("Exploring DBSCAN")
        response_apply = self.exploring_instance.aplicateDBSCAN()
        self.__evaluate_algorithm("DBSCAN", response_apply, "", self.exploring_instance)

        #Meanshift
        print("Exploring Meanshift")
        response_apply = self.exploring_instance.aplicateMeanShift()
        self.__evaluate_algorithm("MeanShift", response_apply, "", self.exploring_instance)

        #Affinity propagation
        print("Exploring AffinityPropagation")
        #response_apply = self.exploring_instance.aplicateAffinityPropagation()
        self.__evaluate_algorithm("AffinityPropagation", response_apply, "", self.exploring_instance)

        #Apply k-means and birch
        print("Exploring k-means and birch")
        self.__exploring_with_k_params()

        #Apply Agglommerative
        print("Exploring Agglommerative")
        self.__exploring_agglomerative_ks()

        #Apply optics
        print("Exploring Optics")
        self.__exploring_optics()

        #Apply
        print("Exporting results")
        self.__export_results()
