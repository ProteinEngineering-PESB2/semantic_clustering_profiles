class developed_model(object):

    def __init__(self, labels, dataset, algorithm, params_list, metrics, status):

        self.labels = labels
        self.dataset = dataset
        self.algorithm = algorithm
        self.param_list = params_list
        self.metrics = metrics
        self.status = status

    def change_status(self, status):
        self.status = status
