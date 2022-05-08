import pandas as pd
from scipy.spatial import distance
import time
import os
import multiprocessing as mp

class estimated_distance(object):
    
    def __init__(self, dataset, name_output):
        self.dataset = dataset
        self.name_output = name_output

        self.__start_variables()

    def __start_variables(self):
        
        #get number of cpu
        self.cpu_number = mp.cpu_count()
        print(self.cpu_number)

        #make ranges between all elements
        self.number_data = int(len(self.dataset)/self.cpu_number)
        self.rest_element = int(len(self.dataset)%self.cpu_number)

        #get index
        self.index_data = []

        for i in range(self.cpu_number):
            start = i*self.number_data
            stop = start+self.number_data

            if i == self.cpu_number-1:
                stop = stop+self.rest_element
            row = [start, stop]
            self.index_data.append(row)

    def create_vector_values(self, dataset, index):

        #hacerlo con pandas para mas facilidad
        row =  [dataset[value][index] for value in dataset.keys() if value != "id"]
        id_value = dataset["id"][index]
        row.insert(0, id_value)
        
        return row
    
    def create_vector_values_multi(self, dataset, start, stop):

        #hacerlo con pandas para mas facilidad
        matrix_row = []
        for i in range(start, stop):
            row =  [dataset[value][index] for value in dataset.keys()]
            matrix_row.append(row)
        return matrix_row
    
    def estimated_distance(self, vector1, vector2):

        id_1 = vector1[0]
        id_2 = vector2[0]
        distance_result = [id_1, id_2, distance.cityblock(vector1[1:], vector2[1:]), distance.cosine(vector1[1:], vector2[1:]), distance.correlation(vector1[1:], vector2[1:])]
        return distance_result
    
    def estimated_distance_multi(self, vector1, matrix_vector):

        distance_results = []

        for vector in matrix_vector:
            distance_value = self.estimated_distance(vector1, vector)
            distance_results.append(distance_value)

        return distance_results
    
    def function_to_estimate_distances(self, dataset, vector_list, start, stop, records_distances):

        print("Start: ", os.getpid())
        for vector1 in vector_list:
            distance_value = self.estimated_distance_multi(vector1, vector_list[start:stop])
            records_distances.append(distance_value)

        print("Finish: ", os.getpid())
    
    def parallelism_create_vector_distance(self, dataset, start, stop, record_vectors):

        for i in range(start, stop):#completo		
            vector1 = self.create_vector_values(dataset, i)
            record_vectors.append(vector1)

    def __export_results(self, records_distances):
        #export data distances
        print("Export results")
        matrix_data = []
        for record_row in records_distances:
            for record in record_row:
                row = [value for value in record]
                matrix_data.append(row)

        print(len(matrix_data))

        data_export = pd.DataFrame(matrix_data, columns=["id_1", "id_2", "euclidean", "cosine", "correlation"])
        data_export.to_csv(self.name_output, index=False)

    def run_parallel(self):
        #star paralelism
        with mp.Manager() as manager:
            
            record_vectors = manager.list([])
            records_distances = manager.list([])

            processes_create_vectors = []
            processes_estimated_distance = []

            print("Init process")
            
            for i in range(self.cpu_number):

                #create vector list (for 1)
                start = self.index_data[i][0]
                stop = self.index_data[i][1]
                print(start, stop)

                #paralelize todos los vectores 01
                tupe_arrays = tuple([self.dataset, start, stop, record_vectors])
                processes_create_vectors.append(mp.Process(target=self.parallelism_create_vector_distance, args=tupe_arrays))
            
            #run and join data process	
            for p in processes_create_vectors:
                print("Start process create vectors")
                p.start()

            for p in processes_create_vectors:
                print("Join data create vectors process")
                p.join()
            
            print(len(record_vectors))

            time.sleep(10)

            for i in range(self.cpu_number):

                start = self.index_data[i][0]
                stop = self.index_data[i][1]
                print(start, stop)

                processes_estimated_distance.append(mp.Process(target=self.function_to_estimate_distances, args=[self.dataset, record_vectors, start, stop, records_distances]))

            for p in processes_estimated_distance:
                print("Start process estimated distance")
                p.start()

            for p in processes_estimated_distance:
                print("Process data join estimated distance")
                p.join()
            
            self.__export_results(records_distances)