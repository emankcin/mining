import unittest
from fitemset.apriori.apriori_straightforward import get_frequent_one_itemsets, apriori_without_hashsets, get_frequent_n_itemsets, itemsets_self_join

class AprioriTest(unittest.TestCase):
    def setUp(self):
        self.dataset = [[0, 1, 2, 3],
                        [0, 1, 2],[0, 1, 3],[0, 2, 3],[1, 2, 3],
                        [1, 2],[1, 3],[2, 3],
                        [3]]
        self.n = 4
        self.f_two_itemsets = {(1, 2): 4, (0, 1): 3, (1, 3): 4, (2, 3): 4, (0, 3): 3, (0, 2): 3,
                               (0,): 4, (1,): 6, (2,): 6, (3,): 7}
        self.f_three_itemsets = {(1, 2): 4, (0, 1): 3, (1, 3): 4, (2, 3): 4, (0, 3): 3, (0, 2): 3,
                                (0,): 4, (1,): 6, (2,): 6, (3,): 7}
        self.f_four_itemsets = {(1, 2): 4, (0,): 4, (2, 3): 4, (1,): 6, (1, 3): 4, (2,): 6, (3,): 7}
        self.f_five_itemsets = {(2,): 6, (3,): 7, (1,): 6}
        self.f_six_itemsets = {(2,): 6, (3,): 7, (1,): 6}
        self.f_seven_itemsets = {(3,): 7}

    def test_get_frequent_one_itemsets(self):
        self.assertEqual({(2,): 6, (0,): 4, (3,): 7, (1,): 6}, get_frequent_one_itemsets(self.dataset, self.n, 3))
        self.assertEqual({(2,): 6, (0,): 4, (3,): 7, (1,): 6}, get_frequent_one_itemsets(self.dataset, self.n, 4))
        self.assertEqual({(2,): 6, (3,): 7, (1,): 6}, get_frequent_one_itemsets(self.dataset, self.n, 5))
        self.assertEqual({(2,): 6, (3,): 7, (1,): 6}, get_frequent_one_itemsets(self.dataset, self.n, 6))
        self.assertEqual({(3,): 7}, get_frequent_one_itemsets(self.dataset, self.n, 7))
        self.assertEqual({}, get_frequent_one_itemsets(self.dataset, self.n, 8))

    def test_apriori(self):
        self.assertEqual(self.f_three_itemsets, apriori_without_hashsets(self.dataset, self.n, 3))
        self.assertEqual(self.f_four_itemsets, apriori_without_hashsets(self.dataset, self.n, 4))
        self.assertEqual(self.f_five_itemsets, apriori_without_hashsets(self.dataset, self.n, 5))
        self.assertEqual(self.f_six_itemsets, apriori_without_hashsets(self.dataset, self.n, 6))
        self.assertEqual(self.f_seven_itemsets, apriori_without_hashsets(self.dataset, self.n, 7))

    def test_itemsets_self_join(self):
        self.assertEqual([[1,2,3,4], [1,2,3,5], [1,2,4,5]], itemsets_self_join([[1,2,3], [6,7,8], [1,2,4], [1,2,5]]).values())

    def test_get_frequent_n_itemsets(self):
        self.assertEqual( [(1, 2), (1,3), (2, 3)], get_frequent_n_itemsets(self.dataset, {0:(1, 2), 1:(1, 3), 2:(2, 3)}, 4).keys())