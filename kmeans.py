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

minValues = [min(dataset[i]) for i in range(dim)]
maxValues = [max(dataset[i]) for i in range(dim)]
dimLengths = list(np.absolute(np.array(maxValues) - np.array(minValues)))

# generate a random point inside the given data range
def generatePoint():
    return [(minValues[i] + np.random.rand() * dimLengths[i]) for i in range(dim)]

# euclidean distance
def dist(x, y):
    return np.sqrt(sum([(x[i] - y[i])**2 for i in range(min(len(x), len(y)))]))

def kmeans(data, k=4):
    centroids = [generatePoint() for i in range(k)]
    centroidsFrame = pd.DataFrame(centroids)
    clusters = [[] for i in range(k)]
    kmeans_h(data, k, centroids, clusters, centroidsFrame)

def kmeans_h(data, k, centroids, clusters, centroidsFrame):
    ax = data.plot(kind="scatter", x=0, y=1, figsize=f_size)
    plotMeans(ax, centroidsFrame, centroids, k)
    plt.show()
    for i in range(k):
        clusters[i] = []
    for i in range(len(dataset)):
        idx = getNearestMeanIndex([data[0][i], data[1][i]], centroids)
        clusters[idx].append([data[0][i], data[1][i]])
    (hasChanged, centroids, centroidsFrame) = updateMeans(clusters, centroids)
    if True == hasChanged:
        kmeans_h(data, k, centroids, clusters, centroidsFrame)        
        for i in range(k):
            for j in range(k):
                if dist(centroids[i], centroids[j]) < 5:
                    centroids[j] = generatePoint()
    
def updateMeans(clusters, centroids):
    flag = False
    for i in range(len(clusters)):
        if clusters[i] == []:
            centroids[i] = generatePoint() 
            continue       
        if flag == False:
            if np.absolute(centroids[i][0] - np.mean(clusters[i], axis=0)[0]) > 0.01:
                flag = True
        centroids[i][0] = np.mean(clusters[i], axis=0)[0]
        centroids[i][1] = np.mean(clusters[i], axis=0)[1]
    centroidsFrame = pd.DataFrame(centroids)
    return (flag, centroids, centroidsFrame)

def getNearestMeanIndex(point, means):
    dists = []
    for mean in means:
        dists.append(dist(point, mean))
    minidx = 0
    for i in range(len(dists)):
        if(dists[i] < dists[minidx]):
            minidx = i
    return minidx

def plotMeans(ax, centroidsFrame, centroids, k):
    centroidsFrame.plot(ax = ax, kind="scatter", x=0, y=1, figsize=f_size, color="red")
    for i in range(k):
        x = centroids[i][0]
        y = centroids[i][1]
        ax.annotate(u'µ_'+str(i+1), xy=(x,y), xytext=(x+dimLengths[0]/float(100),y+dimLengths[1]/float(100)))

kmeans(dataset, k=4)