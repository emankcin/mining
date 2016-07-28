#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame
from scipy.spatial.distance import euclidean

# dimensionality of dataset
DIM = 2
# µ_1 == µ_2 <=> dist(µ_1, µ_2) < EPS
EPS = 0.01

# size of figure: (width, height) in inches
FIG_SIZE = (25, 10)

# euclidean distance
def _dist(x, y):
    return euclidean(x, y)

# returns index in means of neareast mean respective to point
def _get_nearest_mean_index(point, means):
    return np.argmin([_dist(point, mean) for mean in means])

class K_Means:

    """Construct K_Means_Handler object from two-dimensional dataset"""
    def __init__(self, dataset):
        self._dataset = dataset
        self._min_values = [min(self._dataset[i]) for i in range(DIM)]
        self._max_values = [max(self._dataset[i]) for i in range(DIM)]
        self._dim_lengths = [abs(self._max_values[i] - self._min_values[i]) for i in range(DIM)]
   
    """Iteratively computes means of k clusters for data of type DataFrame"""
    def kmeans(self, k=4, visualizeSteps=False):
        # 1) initialize means
        centroids = [self._generate_point() for i in range(k)]
        # 2) start iterative adaptation of means
        self._kmeans_h(k, centroids, visualizeSteps)

    # generate a random point inside the given data range
    def _generate_point(self):
        return [self._min_values[i] + np.random.rand() * self._dim_lengths[i] for i in range(DIM)]

    # plots data and means and updates means until means don't change anymore
    def _kmeans_h(self, k, centroids, visualizeSteps):
        while True:
            if True == visualizeSteps:
                self._plot_data_and_means(centroids, k)
            clusters = [[] for i in range(k)]
            for point in np.array(self._dataset).tolist():
                idx = _get_nearest_mean_index(point, centroids)
                clusters[idx].append(point)
            (means_have_changed, centroids) = self._update_means(clusters, centroids)
            if(False == means_have_changed):
                # plot end result
                self._plot_data_and_means(centroids, k)
                break

    # plots data points and then centroids on top of it
    def _plot_data_and_means(self, centroids, k):
        ax = self._dataset.plot(kind="scatter", x=0, y=1, figsize=FIG_SIZE)
        self._plot_means(ax, centroids, k)
        plt.show()

    # plots annotated means
    def _plot_means(self, ax, centroids, k):
        # plot means
        bx = DataFrame(centroids).plot(ax = ax, kind="scatter", x=0, y=1, figsize=FIG_SIZE, color="red")
        # annotate means
        for i in range(k):
            (x,y) = tuple(centroids[i])
            (offset_x, offset_y) = tuple(np.array(self._dim_lengths)/float(100))
            bx.annotate(u'µ_'+str(i+1), xy=(x,y), xytext=(x+offset_x,y+offset_y))

    # computes new means of clusters and indicates if old and new means differ
    # returns (meansHaveChanged, updatedCentroids)
    def _update_means(self, clusters, centroids):
        flag = False
        for i in range(len(clusters)):
            if clusters[i] == []:
                centroids[i] = self._generate_point()
                flag = True        
            else:
                if flag == False:
                    for j in range(DIM):
                        if abs(centroids[i][j] - np.mean(clusters[i], axis=0)[j]) > EPS:
                            flag = True
                centroids[i] = np.mean(clusters[i], axis=0)
        return (flag, centroids)