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

class K_Means:

    """Construct K_Means object from two-dimensional dataset of type DataFrame"""
    def __init__(self, dataset, k=4):
        self._dataset = dataset
        self._min_values = [min(self._dataset[i]) for i in range(DIM)]
        self._max_values = [max(self._dataset[i]) for i in range(DIM)]
        self._dim_lengths = [abs(self._max_values[i] - self._min_values[i]) for i in range(DIM)]
        self.reinitialize(k)

    """Update object using new value for k"""
    def reinitialize(self, k=4):
        self._k = k
        self._clusters = [[] for i in range(k)]
        self._centroids = [self._generate_point() for i in range(k)]

    """Compute centroids of k clusters"""
    def kmeans(self, visualizeSteps=False):
        while True:
            if visualizeSteps:
                self._visualize_step()
            self._assign_points_to_nearest_centroids()
            result_is_stable = self._update_centroids()
            if result_is_stable:
                # plot end result
                self._visualize_step()
                break

    # generate a random point inside the given data range
    def _generate_point(self):
        return [self._min_values[i] + np.random.rand() * self._dim_lengths[i] for i in range(DIM)]

    # return index of centroid which is nearest to point
    def _get_nearest_centroid_index(self, point):
        return np.argmin([_dist(point, centroid) for centroid in self._centroids])

    def _assign_points_to_nearest_centroids(self):
        self._clusters = [[] for i in range(self._k)]
        for point in np.array(self._dataset).tolist():
            idx = self._get_nearest_centroid_index(point)
            self._clusters[idx].append(point)

    # plot data points and then centroids on top of it
    def _visualize_step(self):
        # plot data points
        ax = self._dataset.plot(kind="scatter", x=0, y=1, figsize=FIG_SIZE)
        # plot annotated centroids on top of data
        self._plot_centroids(ax)
        # show plots
        plt.show()

    # plot annotated centroids
    def _plot_centroids(self, ax):
        # plot centroids
        bx = DataFrame(np.array(self._centroids)).plot(ax = ax, kind="scatter", x=0, y=1, figsize=FIG_SIZE, color="red")
        # annotate centroids
        for i in range(self._k):
            (x,y) = tuple(self._centroids[i])
            (offset_x, offset_y) = tuple(np.array(self._dim_lengths)/float(100))
            bx.annotate(u'µ_'+str(i+1), xy=(x,y), xytext=(x+offset_x,y+offset_y))

    # compute new centroids of clusters and return True if centroids have changed
    def _update_centroids(self):
        stable_result = True
        for i in range(len(self._clusters)):
            if not self._clusters[i]:
                self._centroids[i] = self._generate_point()
                stable_result = False        
            else:
                if stable_result:
                    for j in range(DIM):
                        if abs(self._centroids[i][j] - np.mean(self._clusters[i], axis=0)[j]) > EPS:
                            stable_result = False
                self._centroids[i] = np.mean(self._clusters[i], axis=0)
        return stable_result