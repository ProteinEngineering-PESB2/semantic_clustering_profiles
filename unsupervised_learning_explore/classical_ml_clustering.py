from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import MeanShift
from sklearn.cluster import estimate_bandwidth
from sklearn.cluster import DBSCAN
from sklearn.cluster import Birch
from sklearn.cluster import OPTICS


class aplicateClustering(object):

    def __init__(self, dataSet):
        self.dataSet = dataSet

    #metodo que permite aplicar k-means, genera diversos set de datos con respecto a las divisiones que se emplean...
    def aplicateKMeans(self, numberK):

        try:
            self.model = KMeans(n_clusters=numberK, random_state=1).fit(self.dataSet)
            self.labels = self.model.labels_
            self.number_groups = len(list(set(self.labels)))
            return 0
        except:
            pass
            return 1

    #metodo que permite aplicar bisrch clustering
    def aplicateBirch(self, numberK):

        try:
            self.model = Birch(threshold=0.2, branching_factor=50, n_clusters=numberK, compute_labels=True, copy=True).fit(self.dataSet)
            self.labels = self.model.labels_
            self.number_groups = len(list(set(self.labels)))
            return 0
        except:
            pass
            return 1

    #metodo que permite aplicar cluster jerarquico
    def aplicateAlgomerativeClustering(self, linkage, affinity, numberK):

        try:
            self.model = AgglomerativeClustering(n_clusters=numberK, affinity=affinity, memory=None, connectivity=None, compute_full_tree='auto', linkage=linkage).fit(self.dataSet)
            self.labels = self.model.labels_
            self.number_groups = len(list(set(self.labels)))
            return 0
        except:
            pass
            return 1

    #metodo que permite aplicar AffinityPropagation, con diversos parametros...
    def aplicateAffinityPropagation(self):

        try:
            self.model = AffinityPropagation().fit(self.dataSet)
            self.labels = self.model.labels_
            self.number_groups = len(list(set(self.labels)))
            return 0
        except:
            pass
            return 1

    #metodo que permite aplicar DBSCAN
    def aplicateDBSCAN(self):

        try:
            self.model = DBSCAN(eps=0.3, min_samples=10).fit(self.dataSet)
            self.labels = self.model.labels_
            self.number_groups = len(list(set(self.labels)))
            return 0
        except:
            pass
            return 1

    #metodo que permite aplicar MeanShift clustering...
    def aplicateMeanShift(self):

        try:
            bandwidth = estimate_bandwidth(self.dataSet, quantile=0.2)
            self.model = MeanShift(bandwidth=bandwidth, bin_seeding=True)
            self.model = self.model.fit(self.dataSet)
            self.labels = self.model.labels_
            self.number_groups = len(list(set(self.labels)))
            return 0
        except:
            return 1

    def applicateOptics(self, min_samples, xi, min_cluster_size):
        try:
            self.model = OPTICS(min_samples=min_samples, xi=xi, min_cluster_size=min_cluster_size)
            self.model = self.model.fit(self.dataSet)
            self.labels = self.model.labels_
            self.number_groups = len(list(set(self.labels)))
            return 0
        except:
            return 1