import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#Se importan las bibliotecas de clustering jerárquico
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
#Se importan las bibliotecas de K Means
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

class Clustering(object):
    def __init__(self, df, name, method):
        super().__init__()
        self.df = df
        self.name = name
        self.method = method
        self.x_label = 'Observaciones'
        self.y_label = 'Distancia'
        self.len_columns = len(list(self.df.columns.values))
        self.kmeans_elbow_range = range(2, len_columns) if len_columns > 2 else range(len_columns-1, len_columns) 

    def get_dendogram(self):
        #Se crea el árbol
        plt.figure(figsize=(10, 7))
        plt.title(self.name)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        Arbol = shc.dendrogram(shc.linkage(self.df.values, method='complete'))
        return Arbol

    def get_elbow_method(self):
        SSE = []
        for i in self.kmeans_elbow_range:
            km = KMeans(n_clusters=i, random_state=0)
            km.fit(self.df.values)
            SSE.append(km.inertia_)
        #Se grafica SSE en función de k
        plt.figure(figsize=(10, 7))
        plt.plot(self.kmeans_elbow_range, SSE, marker='o')
        plt.xlabel('Cantidad de clusters *k*')
        plt.ylabel('SSE')
        plt.title('Elbow Method')
        plt.show()
        return 

    def get_visualization_method(self):
        if self.method == "hierachy":
            return self.get_dendogram()
        else:
            return self.get_elbow_method()

    
            
