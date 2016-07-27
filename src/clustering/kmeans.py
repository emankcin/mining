#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# dimensionality of the data
DIM = 2
# resolution of the data
EPS = 0.01

_csv_path = "2d-sample.csv"
_delimiter = ","
_engine = "python"
_f_size = (25, 10)

_dataset = pd.read_csv(_csv_path, "r", delimiter=_delimiter, engine=_engine, header=None)

_min_values = [min(_dataset[i]) for i in range(DIM)]
_max_values = [max(_dataset[i]) for i in range(DIM)]
_dim_lengths = list(np.absolute(np.array(_max_values) - np.array(_min_values)))

"""Iteratively computes k means of clusters for data of type DataFrame"""
def kmeans(data, k=4):
    # 1) initialize means
    centroids = [_generate_point() for i in range(k)]
    centroids = pd.DataFrame(centroids).transpose()
    # 2) start iterative adaptation of means
    _kmeans_h(data, k, centroids)

# euclidean distance
def _dist(x, y):
    return np.sqrt(sum([(x[i] - y[i])**2 for i in range(DIM)]))

# generate a random point inside the given data range
def _generate_point():
    return [(_min_values[i] + np.random.rand() * _dim_lengths[i]) for i in range(DIM)]

# plots data points and then centroids on top of it
def _plot_data_and_means(data, centroids, k):
    ax = data.plot(kind="scatter", x=0, y=1, figsize=_f_size)
    _plot_means(ax, centroids, k)
    plt.show()

# plots data and means and updates means until means don't change anymore
def _kmeans_h(data, k, centroids):
    means_have_changed = True
    while means_have_changed == True:
        _plot_data_and_means(data, centroids, k)
        clusters = [[] for i in range(k)]
        for i in data.transpose():
            point = list(data.transpose()[i])
            idx = _get_nearest_mean_index(point, centroids)
            clusters[idx].append(point)
        (means_have_changed, centroids) = _update_means(clusters, centroids)
    
def _update_means(clusters, centroids):
    flag = False
    for i in range(len(clusters)):
        if clusters[i] == []:
            centroids[i] = _generate_point() 
            continue       
        if flag == False:
            if np.absolute(centroids[i][0] - np.mean(clusters[i], axis=0)[0]) > EPS:
                flag = True
        centroids[i][0] = np.mean(clusters[i], axis=0)[0]
        centroids[i][1] = np.mean(clusters[i], axis=0)[1]
    return (flag, centroids)

def _get_nearest_mean_index(point, means):
    dists = []
    for idx in means:
        dists.append(_dist(point, means[idx]))
    min_idx = 0
    for i in range(len(dists)):
        if(dists[i] < dists[min_idx]):
            min_idx = i
    return min_idx

def _plot_means(ax, centroids, k):
    centroids.transpose().plot(ax = ax, kind="scatter", x=0, y=1, figsize=_f_size, color="red")
    for i in range(k):
        x = centroids[i][0]
        y = centroids[i][1]
        offset_x = _dim_lengths[0]/float(100)
        offset_y = _dim_lengths[1]/float(100)
        ax.annotate(u'µ_'+str(i+1), xy=(x,y), xytext=(x+offset_x,y+offset_y))

kmeans(_dataset, k=4)