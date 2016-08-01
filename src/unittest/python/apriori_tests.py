import unittest
from fitemset.executor import get_frequent_one_itemsets, apriori_without_hashsets

class AprioriTest(unittest.TestCase):
    def setUp(self):
        self.dataset = [[0, 1, 2],[0, 1, 3],[0, 2, 3],[1, 2, 3],
                        [2, 3],[1, 2],[1, 3],
                        [3]]
        self.n = 4
        self.f_three_itemsets = [[0], [1], [2], [3],
                       [1, 2], [1, 3], [2, 3]]

    def test_get_frequent_one_itemsets(self):
        self.assertEqual([[0], [1], [2], [3]], get_frequent_one_itemsets(self.dataset, self.n, 3))
        self.assertEqual([[1], [2], [3]], get_frequent_one_itemsets(self.dataset, self.n, 4))
        self.assertEqual([[1], [2], [3]], get_frequent_one_itemsets(self.dataset, self.n, 5))
        self.assertEqual([[3]], get_frequent_one_itemsets(self.dataset, self.n, 6))
        self.assertEqual([], get_frequent_one_itemsets(self.dataset, self.n, 7))

    def test_apriori(self):
        self.assertEqual(self.f_three_itemsets, apriori_without_hashsets(self.dataset, self.n, 3))