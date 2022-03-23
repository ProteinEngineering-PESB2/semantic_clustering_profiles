from sklearn import metrics

class evaluationClustering(object):

    def __init__(self, dataSet, labelsResponse):

        self.dataSet = dataSet
        self.labelsResponse = labelsResponse
        try:
            self.calinski = metrics.calinski_harabasz_score(self.dataSet, self.labelsResponse)
            self.siluetas = metrics.silhouette_score(self.dataSet, self.labelsResponse, metric='euclidean')
            self.davies = metrics.davies_bouldin_score(self.dataSet, self.labelsResponse)
        except:
            self.calinski = "ERROR"
            self.siluetas = "ERROR"
            self.davies = "ERROR"
            pass