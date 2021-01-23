import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
#Se importan las bibliotecas de clustering jerárquico
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
#Se importan las bibliotecas de K Means
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

from kneed import KneeLocator

class Clustering(object):
    """
    Clase que implementa los dos métodos de clustering.
    """    
    def __init__(self, df, name, method):
        """
        Esta clase necesita:
        Args:
            df (dataframe): Dataframe de pandas que contiene la información numérica para hacer el clustering.
            name (str): [description]
            method ([type]): [description]
        """        
        self.df = df.copy()
        self.name = name
        self.method = method
        self.x_label = 'Observaciones'
        self.y_label = 'Distancia'
        self.len_columns = len(list(self.df.columns.values))
        self.decimal_round = 3
        self.elbow_range = range(2, self.len_columns) if self.len_columns > 2 else range(self.len_columns-1, self.len_columns) 

    def get_agglomerative_clusters(self,n_clusters, affinity='euclidean', linkage='complete'):
        MJerarquico = AgglomerativeClustering(n_clusters=n_clusters, affinity=affinity, linkage=linkage)
        MJerarquico.fit_predict(self.df.values)
        return MJerarquico

    def get_kmeans_clusters(self,n_clusters, random_state=0):
        km = KMeans(n_clusters=n_clusters, random_state=random_state)
        km.fit(self.df.values)
        return km

    def get_dendogram(self):
        figure = plt.figure()
        plt.title(self.name)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        shc.dendrogram(shc.linkage(self.df.values, method='complete'))
        return figure

    def get_kmeans_visualization_method(self):
        SSE = self.get_clustering_list(self.get_kmeans_clusters)
        figure = plt.figure()
        plt.plot(self.elbow_range, SSE, marker='o')
        plt.xlabel('Cantidad de clusters *k*')
        plt.ylabel('SSE')
        plt.title('Elbow Method')
        return figure

    def get_clustering_list(self, function):
        SSE = []
        for i in self.elbow_range:
            algorithm = function(i)
            algorithm.fit(self.df.values)
            SSE.append(algorithm.inertia_) 
        return SSE

    def get_visualization_method(self):
        if self.method == "hierarchy":
            return self.get_dendogram()
        else:
            return self.get_kmeans_visualization_method()

    def get_elbow_method(self, function):
        SSE = self.get_clustering_list(function)
        knee = KneeLocator(self.elbow_range, SSE, curve="convex", direction="decreasing")    
        return knee.elbow

    def get_heuristic_method(self):
        if self.method == "hierarchy":
            return self.get_elbow_method(self.get_agglomerative_clusters)
        else:
            return self.get_elbow_method(self.get_kmeans_clusters)

    def get_cluster_summary(self, function, n_clusters):
        try:
            clusters = function(n_clusters)
        except ValueError:
            raise ValueError("El número de clusters excede el número de registros {}>{}".format(n_clusters,self.df.shape[0]) )
        self.df['clusterH'] = clusters.labels_
        mean = self.df.groupby(['clusterH']).mean()
        mean["#Registros"] = self.df.groupby(['clusterH'])['clusterH'].count()
        mean["#Cluster"] = pd.Series(data=range(0,len(mean["#Registros"])))
        mean_ordered = mean.reindex(sorted(mean.columns), axis=1) 
        self.cluster_df = mean_ordered
        return mean_ordered

    def get_clusters(self, n_clusters):
        if self.method == "hierarchy":
            return self.get_cluster_summary(self.get_agglomerative_clusters, n_clusters)
        else:
            return self.get_cluster_summary(self.get_kmeans_clusters, n_clusters)
        return

    def get_export_file(self):
        file = StringIO()
        self.cluster_df.round(self.decimal_round).to_csv(file)
        return file.getvalue()

    def get_scatter_plot(self):
        cluster = "clusterH"
        columns = list(self.df.columns.values)
        columns.remove(cluster)
        values = self.df[columns].values
        labels = self.df[cluster].values
        figure = plt.figure(figsize=(10, 7))
        plt.scatter(values[:,0], values[:,1], c=labels, cmap='rainbow')
        plt.grid()
        plt.title("Gráfica de clusters")
        return figure