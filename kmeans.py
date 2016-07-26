#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

csv_path = "2d-sample.csv"
dim = 2
delimiter = ","
engine = "python"
f_size = (25, 10)

dataset = pd.read_csv(csv_path, "r", delimiter=delimiter, engine=engine, header=None)

minX = min(dataset[0])
minY = min(dataset[1])
maxX = max(dataset[0])
maxY = max(dataset[1])
xDist = np.absolute(maxX - minX)
yDist = np.absolute(maxY - minY)


def kmeans(data, k=4):
    centroids = []  
    for i in range(k):
        centroids.append([minX + np.random.rand() * xDist, minY + np.random.rand() * yDist])
    mus = pd.DataFrame(centroids)
    clusters = []
    for i in range(k):
        clusters.append([])
    kmeans_h(data, k, centroids, clusters, mus)

def kmeans_h(data, k, centroids, clusters, mus):
    ax = data.plot(kind="scatter", x=0, y=1, figsize=f_size)
    plotMeans(ax, mus, centroids, k)
    plt.show()
    for i in range(k):
        clusters[i] = []
    for i in range(len(dataset)):
        idx = getNearestMeanIndex([data[0][i], data[1][i]], centroids)
        clusters[idx].append([data[0][i], data[1][i]])
    (hasChanged, centroids, mus) = updateMeans(clusters, centroids)
    if True == hasChanged:
        kmeans_h(data, k, centroids, clusters, mus)        
        for i in range(k):
            for j in range(k):
                if (centroids[i][0] - centroids[j][0])**2 + (centroids[i][1] - centroids[j][1])**2 < 5:
                    centroids[j] = [minX + np.random.rand() * xDist, minY + np.random.rand() * yDist]
    
def updateMeans(clusters, centroids):
    flag = False
    for i in range(len(clusters)):
        if clusters[i] == []:
            centroids[i] = [minX + np.random.rand() * xDist, minY + np.random.rand() * yDist] 
            continue       
        if flag == False:
            if np.absolute(centroids[i][0] - np.mean(clusters[i], axis=0)[0]) > 0.01:
                flag = True
        centroids[i][0] = np.mean(clusters[i], axis=0)[0]
        centroids[i][1] = np.mean(clusters[i], axis=0)[1]
    mus = pd.DataFrame(centroids)
    return (flag, centroids, mus)

def getNearestMeanIndex(point, means):
    dists = []
    for mean in means:
        dists.append((point[0] - mean[0])**2 + (point[1] - mean[1])**2)
    minidx = 0
    for i in range(len(dists)):
        if(dists[i] < dists[minidx]):
            minidx = i
    return minidx

def plotMeans(ax, mus, centroids, k):
    mus.plot(ax = ax, kind="scatter", x=0, y=1, figsize=f_size, color="red")
    for i in range(k):
        x = centroids[i][0]
        y = centroids[i][1]
        ax.annotate(u'µ_'+str(i+1), xy=(x,y), xytext=(x+0.2,y+0.2))

kmeans(dataset, k=5)