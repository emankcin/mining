import pandas as pd
import unittest

from kdd.clustering.kmeans import KMeans, _dist


class KMeansTest(unittest.TestCase):
    def setUp(self):
        dataset = pd.DataFrame([[1, 2], [3, 4], [4, 5], [6, 7]])
        self.k = 4
        self.k_means = KMeans(dataset, k=self.k)

    def test_reinitialize(self):
        new_k = 10
        self.k_means.reinitialize(k=new_k)
        self.assertEqual(new_k, self.k_means.k)
        self.assertEqual(new_k, len(self.k_means.clusters))
        self.assertEqual(new_k, len(self.k_means.centroids))

    def test_kmeans(self):
        self.k_means.kmeans(visualizeSteps=0)
        self.assertEqual(self.k, self.k_means.k)
        self.assertEqual(self.k, len(self.k_means.clusters))
        self.assertEqual(self.k, len(self.k_means.centroids))

    def test_dist(self):
        self.assertEqual(2, int(round(_dist([0, 0], [1, 1]) * _dist([1, 1], [2, 2]))))
        self.assertEqual(0, int(round(_dist([1, 1], [1, 1]))))
