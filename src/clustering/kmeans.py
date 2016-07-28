#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

CSV_PATH = "../../data/2d-sample.csv"
CSV_COLUMN_DELIMITER = ","

# dimensionality of dataset
DIM = 2
# µ_1 == µ_2 <=> dist(µ_1, µ_2) < EPS
EPS = 0.01

# size of figure: (width, height) in inches
FIG_SIZE = (25, 10)

class K_Means_Handler:

    """Construct kmeans object"""
    def __init__(self, dataset):
        self._dataset = dataset
        self._min_values = [min(self._dataset[i]) for i in range(DIM)]
        self._max_values = [max(self._dataset[i]) for i in range(DIM)]
        self._dim_lengths = list(abs(np.array(self._max_values) - np.array(self._min_values)))
   
    """Iteratively computes k means of clusters for data of type DataFrame"""
    def kmeans(self, k=4):
        # 1) initialize means
        centroids = [self._generate_point() for i in range(k)]
        # 2) start iterative adaptation of means
        self._kmeans_h(k, centroids)

    # euclidean distance
    def _dist(self, x, y):
        return np.sqrt(sum([(x[i] - y[i])**2 for i in range(DIM)]))

    # generate a random point inside the given data range
    def _generate_point(self):
        return [(self._min_values[i] + np.random.rand() * self._dim_lengths[i]) for i in range(DIM)]

    # plots data points and then centroids on top of it
    def _plot_data_and_means(self, centroids, k):
        ax = self._dataset.plot(kind="scatter", x=0, y=1, figsize=FIG_SIZE)
        self._plot_means(ax, centroids, k)
        plt.show()

    # plots data and means and updates means until means don't change anymore
    def _kmeans_h(self, k, centroids):
        means_have_changed = True
        while means_have_changed == True:
            self._plot_data_and_means(centroids, k)
            clusters = [[] for i in range(k)]
            for i in self._dataset.transpose():
                point = [self._dataset[0][i], self._dataset[1][i]]
                idx = self._get_nearest_mean_index(point, centroids)
                clusters[idx].append(point)
            (means_have_changed, centroids) = self._update_means(clusters, centroids)

    # computes the new means of clusters and indicates if old and new means differ
    # returns (meansHaveChanged, updatedCentroids)
    def _update_means(self, clusters, centroids):
        flag = False
        for i in range(len(clusters)):
            if clusters[i] == []:
                centroids[i] = self._generate_point() 
                continue       
            if flag == False:
                if abs(centroids[i][0] - np.mean(clusters[i], axis=0)[0]) > EPS:
                    flag = True
            centroids[i][0] = np.mean(clusters[i], axis=0)[0]
            centroids[i][1] = np.mean(clusters[i], axis=0)[1]
        return (flag, centroids)

    # returns index in means of neareast mean respective to point
    def _get_nearest_mean_index(self, point, means):
        dists = []
        for mean in means:
            dists.append(self._dist(point, mean))
        min_idx = 0
        for i in range(len(dists)):
            if(dists[i] < dists[min_idx]):
                min_idx = i
        return min_idx

    # plots annotated means
    def _plot_means(self, ax, centroids, k):
        # plot means
        pd.DataFrame(centroids).plot(ax = ax, kind="scatter", x=0, y=1, figsize=FIG_SIZE, color="red")
        # annotate means
        for i in range(k):
            x = centroids[i][0]
            y = centroids[i][1]
            offset_x = self._dim_lengths[0]/float(100)
            offset_y = self._dim_lengths[1]/float(100)
            ax.annotate(u'µ_'+str(i+1), xy=(x,y), xytext=(x+offset_x,y+offset_y))

def _load_data(path, delim):
        engine = "python"
        dataset = pd.read_csv(path, "r", delimiter=delim, engine=engine, header=None)
        return dataset

"""Apply kmeans to dataset"""
def main():
    dataset = _load_data(CSV_PATH, CSV_COLUMN_DELIMITER)
    km = K_Means_Handler(dataset)
    km.kmeans(k=4)

if __name__ == "__main__":
    main()