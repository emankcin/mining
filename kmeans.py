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

mu0 = np.random.rand(k, dim) * dataset.max()[0]
mu = pd.DataFrame(mu0)

def kmeans(data, k):
    ax = data.plot(kind="scatter", x=0, y=1, figsize=f_size)
    plotMeans(ax, mu, mu0, k)
    plt.show()
    

def plotMeans(ax, mu, mu0, k):
    mu.plot(ax = ax, kind="scatter", x=0, y=1, figsize=f_size, color="red")
    for i in range(k):
        x = mu0[i][0]
        y = mu0[i][1]
        ax.annotate(u'µ_'+str(i+1), xy=(x,y), xytext=(x+0.2,y+0.2))
        
    
kmeans(dataset, 5)
