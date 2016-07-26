#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

k = 5

csv_path = "2d-sample.csv"
dim = 2
delimiter = ","
engine = "python"
f_size = (25, 10)

dataset = pd.read_csv(csv_path, "r", delimiter=delimiter, engine=engine, header=None)

mu0 = np.random.rand(k, dim)
for i in range(k):
    mu0[i] = mu0[i] * ((i+1) / float(k)) * dataset.max() - dataset.max()/2
mu = pd.DataFrame(mu0)
clusters = []
for i in range(k):
    clusters.append([])

def kmeans(data, k):
    ax = data.plot(kind="scatter", x=0, y=1, figsize=f_size)
    plotMeans(ax, mu, mu0, k)
    plt.show()
    for i in range(k):
        clusters[i] = []
    for i in range(len(dataset)):
        idx = getNearestMeanIndex([data[0][i], data[0][i]], mu0)
        clusters[idx].append([data[0][i], data[1][i]])
    hasChanged = updateMeans(clusters)
    if True == hasChanged:
        kmeans(data, k)

def updateMeans(clusters):
    global mu0
    global mu
    flag = False
    for i in range(len(clusters)):
        if clusters[i] == []:
            continue
        if flag == False:
            if np.absolute(mu0[i][0] - np.mean(clusters[i], axis=0)[0]) > 0.01:
                flag = True
        mu0[i] = np.mean(clusters[i], axis=0)
    mu = pd.DataFrame(mu0)
    return flag

def getNearestMeanIndex(point, means):
    dists = []
    for mean in means:
        dists.append((point[0] - mean[0])**2 + (point[1] - mean[1])**2)
    minidx = 0
    for i in range(len(dists)):
        if(dists[i] < dists[minidx]):
            minidx = i
    return minidx

def plotMeans(ax, mu, mu0, k):
    mu.plot(ax = ax, kind="scatter", x=0, y=1, figsize=f_size, color="red")
    for i in range(k):
        x = mu0[i][0]
        y = mu0[i][1]
        ax.annotate(u'µ_'+str(i+1), xy=(x,y), xytext=(x+0.2,y+0.2))
        
    
kmeans(dataset, 5)
