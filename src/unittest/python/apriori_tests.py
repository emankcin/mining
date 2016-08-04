from fitemset.apriori.apriori import get_frequent_one_itemsets, apriori, \
    get_frequent_n_itemsets, itemsets_self_join, construct_hash_tree, get_f_n_itemsets_w_hashtree
from fitemset_testbase import FItemsetTestBase


class AprioriTest(FItemsetTestBase):

    def test_get_frequent_one_itemsets(self):
        self.assertEqual({(2,): 6, (0,): 4, (3,): 7, (1,): 6}, get_frequent_one_itemsets(self.dataset, self.n, 3))
        self.assertEqual({(2,): 6, (0,): 4, (3,): 7, (1,): 6}, get_frequent_one_itemsets(self.dataset, self.n, 4))
        self.assertEqual({(2,): 6, (3,): 7, (1,): 6}, get_frequent_one_itemsets(self.dataset, self.n, 5))
        self.assertEqual({(2,): 6, (3,): 7, (1,): 6}, get_frequent_one_itemsets(self.dataset, self.n, 6))
        self.assertEqual({(3,): 7}, get_frequent_one_itemsets(self.dataset, self.n, 7))
        self.assertEqual({}, get_frequent_one_itemsets(self.dataset, self.n, 8))

    def test_apriori_with_hash_tree(self):
        self.assertEqual(self.f_three_itemsets, apriori(self.dataset, self.n, 3, with_hash_tree=True))
        self.assertEqual(self.f_four_itemsets, apriori(self.dataset, self.n, 4, with_hash_tree=True))
        self.assertEqual(self.f_five_itemsets, apriori(self.dataset, self.n, 5, with_hash_tree=True))
        self.assertEqual(self.f_six_itemsets, apriori(self.dataset, self.n, 6, with_hash_tree=True))
        self.assertEqual(self.f_seven_itemsets, apriori(self.dataset, self.n, 7, with_hash_tree=True))

    def test_apriori_without_hash_tree(self):
        self.assertEqual(self.f_three_itemsets, apriori(self.dataset, self.n, 3, with_hash_tree=False))
        self.assertEqual(self.f_four_itemsets, apriori(self.dataset, self.n, 4, with_hash_tree=False))
        self.assertEqual(self.f_five_itemsets, apriori(self.dataset, self.n, 5, with_hash_tree=False))
        self.assertEqual(self.f_six_itemsets, apriori(self.dataset, self.n, 6, with_hash_tree=False))
        self.assertEqual(self.f_seven_itemsets, apriori(self.dataset, self.n, 7, with_hash_tree=False))

    def test_itemsets_self_join(self):
        self.assertEqual([[1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 4, 5]],
                         itemsets_self_join([[1, 2, 3], [6, 7, 8], [1, 2, 4], [1, 2, 5]]).values())

    def test_get_frequent_n_itemsets(self):
        current_dictionary = {0: (1, 2), 1: (1, 3), 2: (2, 3)}
        min_sup = 4
        self.assertEqual([(1, 2), (1, 3), (2, 3)],
                         get_frequent_n_itemsets(self.dataset, current_dictionary, min_sup).keys())

    def test_construct_hash_tree(self):
        ht = construct_hash_tree({0: (1, 2), 1: (2, 3)})
        self.assertTrue(ht.contains((1, 2)))
        self.assertFalse(ht.contains((1, 3)))

    def test_get_f_n_itemsets_w_hashtree(self):
        ht = construct_hash_tree({0: (1, 2), 1: (1, 3), 2: (2, 3)})
        min_sup = 4
        self.assertEqual({(1, 2): 4, (2, 3): 4, (1, 3): 4}, get_f_n_itemsets_w_hashtree(self.dataset, ht, min_sup))
