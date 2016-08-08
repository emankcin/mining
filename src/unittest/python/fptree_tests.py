from fitemset_testbase import FItemsetTestBase
from kdd.fitemset.fptree.fptree import FrequentPatternTree, _get_desc_list_of_frequent_one_items, _rearrange_data_set_according_to_one_items, _generate_frequent_pattern_tree

class FPTreeTest(FItemsetTestBase):

    def setUp(self):
        self.data_set = [[1], [2],
                   [1,2], [1,3], [1,4], [3,4],
                   [1,2,4], [1,3,4]]

    def test_get_desc_list_of_frequent_one_items(self):
        self.assertEqual([1,4,2,3], _get_desc_list_of_frequent_one_items(self.data_set, 3))
        self.assertEqual([1,4], _get_desc_list_of_frequent_one_items(self.data_set, 4))
        self.assertEqual([], _get_desc_list_of_frequent_one_items(self.data_set, 10))

    def test_rearrange_data_set_according_to_one_items(self):
        min_sup = 3
        rearranged_data_set = [[1], [2],
                               [1,2], [1,3], [1,4], [4,3],
                               [1,4,2], [1,4,3]]
        self.assertEqual(rearranged_data_set, _rearrange_data_set_according_to_one_items(self.data_set, [1,4,2,3]))

    def test_generate_frequent_pattern_tree(self):
        min_sup = 3
        rearranged_data_set = [[1], [2],
                               [1, 2], [1, 3], [1, 4], [4, 3],
                               [1, 4, 2], [1, 4, 3]]
        fpt = _generate_frequent_pattern_tree(self, rearranged_data_set)
        for item_list in rearranged_data_set:
            for item in item_list:
                self.assertTrue(fpt.contains(item))

    def test_contains_elements_of_inserted_lists(self):
        fpt = FrequentPatternTree()
        for item_list in self.data_set:
            fpt.insert(item_list)
        for item_list in self.data_set:
            for item in item_list:
                self.assertTrue(fpt.contains(item))

