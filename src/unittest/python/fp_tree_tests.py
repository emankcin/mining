from fp_tree_testbase import FPTreeTestBase
from kdd.fitemset.fptree.fp_tree import FrequentPatternTree
from kdd.fitemset.fptree.fp_tree_algorithm import _generate_frequent_pattern_tree


class FPTreeTest(FPTreeTestBase):
    def setUp(self):
        self.data_set = [[1], [2],
                         [1, 2], [1, 3], [1, 4], [3, 4],
                         [1, 2, 4], [1, 3, 4]]
        self.min_sup = 3
        self.rearranged_data_set = [[1], [2],
                                    [1, 2], [1, 3], [1, 4], [4, 3],
                                    [1, 4, 2], [1, 4, 3]]
        self.result = {(1,), (2,), (3,), (4,), (1, 4)}

    def test_pattern_tree_string(self):
        fpt_multi_path = _generate_frequent_pattern_tree(self.rearranged_data_set)
        fpt_multi_path_str = ("-1:1\n"
                              "   1:6\n"
                              "      2:1\n"
                              "      3:1\n"
                              "      4:3\n"
                              "         2:1\n"
                              "         3:1\n"
                              "   2:1\n"
                              "   4:1\n"
                              "      3:1")
        self.assertEqual(fpt_multi_path_str, fpt_multi_path.__str__())
        fpt_single_path = _generate_frequent_pattern_tree([[1, 2, 3], [1, 2], [1, 2, 3, 4], [1], [1, 2, 3]])
        fpt_single_path_str = ("-1:1\n"
                               "   1:5\n"
                               "      2:4\n"
                               "         3:3\n"
                               "            4:1")
        self.assertEqual(fpt_single_path_str, fpt_single_path.__str__())

    def test_pattern_tree_equality(self):
        fpt_1 = _generate_frequent_pattern_tree(self.rearranged_data_set)
        fpt_2 = _generate_frequent_pattern_tree(self.rearranged_data_set)
        fpt_3 = _generate_frequent_pattern_tree(self.data_set)
        self.assertEqual(fpt_1, fpt_2)
        self.assertEqual(fpt_2, fpt_1)
        self.assertNotEqual(fpt_1, fpt_3)
        self.assertNotEqual(fpt_3, fpt_1)
        self.assertNotEqual(fpt_2, fpt_3)
        self.assertNotEqual(fpt_3, fpt_2)
        self.assertEqual(fpt_1, fpt_1)
        self.assertEqual(fpt_2, fpt_2)
        self.assertEqual(fpt_3, fpt_3)

    def test_pattern_tree_is_single_path(self):
        single_path_example = _generate_frequent_pattern_tree([[1, 2, 3], [1, 2, 3], [1, 2], [1]])
        not_single_path_example = _generate_frequent_pattern_tree([[1, 2, 3], [1, 2, 4]])
        another_single_path_example = _generate_frequent_pattern_tree([[1, 2, 3], [1, 2, 3]])
        self.assertEqual([1, 2], single_path_example._is_frequent_single_path(self.min_sup))
        self.assertFalse(not_single_path_example._is_frequent_single_path(self.min_sup))
        self.assertEqual([1], another_single_path_example._is_frequent_single_path(self.min_sup))

    def test_retrieve_frequent_item_sets_of_single_path(self):
        fpt_1 = _generate_frequent_pattern_tree(self.rearranged_data_set)
        fpt_2 = _generate_frequent_pattern_tree([[1, 2, 3], [1, 2], [1, 2]])
        self.assertFalse(fpt_1._retrieve_frequent_item_sets_of_single_path(3))
        self.assertEqual({(1, 2), (2,), (1,)}, fpt_2._retrieve_frequent_item_sets_of_single_path(3))

    def test_contains_elements_of_inserted_lists(self):
        fpt = FrequentPatternTree(-1, [])
        for item_list in self.data_set:
            fpt._insert(item_list, [])
        for item_list in self.data_set:
            for item in item_list:
                self.assertTrue(fpt._contains(item))
