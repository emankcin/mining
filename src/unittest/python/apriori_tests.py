from kdd.fitemset.apriori.apriori import _retrieve_frequent_singleton_counts, apriori, \
    _get_frequent_n_item_tuples_with_counts, _item_lists_self_join, _construct_hash_tree, _get_frequent_n_item_tuples_with_counts_by_hash_tree, _get_frequent_n_item_lists
from fitemset_testbase import FItemsetTestBase


class AprioriTest(FItemsetTestBase):

    def test_apriori_with_hash_tree(self):
        self.assertEqual(self.f_three_item_sets, apriori(self.data_set, 3, with_hash_tree=True))
        self.assertEqual(self.f_four_item_sets, apriori(self.data_set, 4, with_hash_tree=True))
        self.assertEqual(self.f_five_item_sets, apriori(self.data_set, 5, with_hash_tree=True))
        self.assertEqual(self.f_six_item_sets, apriori(self.data_set, 6, with_hash_tree=True))
        self.assertEqual(self.f_seven_item_sets, apriori(self.data_set, 7, with_hash_tree=True))

    def test_apriori_without_hash_tree(self):
        self.assertEqual(self.f_three_item_sets, apriori(self.data_set, 3, with_hash_tree=False))
        self.assertEqual(self.f_four_item_sets, apriori(self.data_set, 4, with_hash_tree=False))
        self.assertEqual(self.f_five_item_sets, apriori(self.data_set, 5, with_hash_tree=False))
        self.assertEqual(self.f_six_item_sets, apriori(self.data_set, 6, with_hash_tree=False))
        self.assertEqual(self.f_seven_item_sets, apriori(self.data_set, 7, with_hash_tree=False))

    def test_retrieve_singleton_counts(self):
        self.assertEqual({(2,): 6, (0,): 4, (3,): 7, (1,): 6}, _retrieve_frequent_singleton_counts(self.data_set, 3))
        self.assertEqual({(2,): 6, (0,): 4, (3,): 7, (1,): 6}, _retrieve_frequent_singleton_counts(self.data_set, 4))
        self.assertEqual({(2,): 6, (3,): 7, (1,): 6}, _retrieve_frequent_singleton_counts(self.data_set, 5))
        self.assertEqual({(2,): 6, (3,): 7, (1,): 6}, _retrieve_frequent_singleton_counts(self.data_set, 6))
        self.assertEqual({(3,): 7}, _retrieve_frequent_singleton_counts(self.data_set, 7))
        self.assertEqual({}, _retrieve_frequent_singleton_counts(self.data_set, 8))

    def test_item_lists_self_join(self):
        self.assertEqual([[1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 4, 5]],
                         _item_lists_self_join([[1, 2, 3], [6, 7, 8], [1, 2, 4], [1, 2, 5]]))

    def test_get_frequent_n_item_tuples_with_counts(self):
        current_list = [[1, 2], [1, 3], [2, 3]]
        min_sup = 4
        self.assertEqual({(1, 2): 4, (1, 3): 4, (2, 3): 4},
                         _get_frequent_n_item_tuples_with_counts(self.data_set, current_list, min_sup))

    def test_get_frequent_n_item_lists(self):
        current_list = [[1, 2], [1, 3], [2, 3]]
        min_sup = 4
        self.assertEqual([[1, 2], [1, 3], [2, 3]],
                         _get_frequent_n_item_lists(self.data_set, current_list, min_sup))

    def test_construct_hash_tree(self):
        ht = _construct_hash_tree([[1, 2], [2, 3]])
        self.assertTrue(ht._contains((1, 2)))
        self.assertFalse(ht._contains((1, 3)))

    def test_get_frequent_n_item_tuples_with_counts_by_hash_tree(self):
        ht = _construct_hash_tree([[1, 2], [1, 3], [2, 3]])
        min_sup = 4
        self.assertEqual({(1, 2): 4, (2, 3): 4, (1, 3): 4}, _get_frequent_n_item_tuples_with_counts_by_hash_tree(self.data_set, ht, min_sup))
