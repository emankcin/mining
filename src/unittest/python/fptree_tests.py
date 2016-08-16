from fitemset_testbase import FItemsetTestBase
from kdd.fitemset.fptree.fptree import FrequentPatternTree, _get_desc_list_of_frequent_one_items, _rearrange_data_set_according_to_one_items, _generate_frequent_pattern_tree, _construct_pattern_base, _convert_pattern_base_to_list_of_conditional_fp_trees, _mine_fp_tree, retrieve
class FPTreeTest(FItemsetTestBase):

    def setUp(self):
        self.data_set = [[1], [2],
                         [1,2], [1,3], [1,4], [3,4],
                         [1,2,4], [1,3,4]]
        self.min_sup = 3
        self.rearranged_data_set = [[1], [2],
                                    [1, 2], [1, 3], [1, 4], [4, 3],
                                    [1, 4, 2], [1, 4, 3]]
        self.result = {(1,), (2,), (3,), (4,), (1, 4)}

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

    def test_get_desc_list_of_frequent_one_items(self):
        self.assertEqual([1,4,2,3], _get_desc_list_of_frequent_one_items(self.data_set, self.min_sup))
        self.assertEqual([1,4], _get_desc_list_of_frequent_one_items(self.data_set, 4))
        self.assertEqual([], _get_desc_list_of_frequent_one_items(self.data_set, 10))

    def test_rearrange_data_set_according_to_one_items(self):
        self.assertEqual(self.rearranged_data_set, _rearrange_data_set_according_to_one_items(self.data_set, [1, 4, 2, 3]))

    def test_generate_frequent_pattern_tree(self):
        fpt = _generate_frequent_pattern_tree(self.rearranged_data_set)

        for item_list in self.rearranged_data_set:
            for item in item_list:
                self.assertTrue(fpt.contains(item))

        self.assertEqual(-1, fpt.value)
        self.assertEqual([], fpt.prefix)
        self.assertEqual([1,2,4], fpt.children.keys())
        self.assertEqual(1, fpt.count)

        fpt_1 = fpt.children[1]
        self.assertEqual(1, fpt_1.value)
        self.assertEqual([], fpt_1.prefix)
        self.assertEqual([2, 3, 4], fpt_1.children.keys())
        self.assertEqual(6, fpt_1.count)

        fpt_1_4 = fpt_1.children[4]
        self.assertEqual(4, fpt_1_4.value)
        self.assertEqual([1], fpt_1_4.prefix)
        self.assertEqual([2,3], fpt_1_4.children.keys())
        self.assertEqual(3, fpt_1_4.count)

        fpt_1_4_2 = fpt_1_4.children[2]
        self.assertEqual(2, fpt_1_4_2.value)
        self.assertEqual([1,4], fpt_1_4_2.prefix)
        self.assertEqual([], fpt_1_4_2.children.keys())
        self.assertEqual(1, fpt_1_4_2.count)

        fpt_2 = fpt.children[2]
        self.assertEqual(2, fpt_2.value)
        self.assertEqual([], fpt_2.prefix)
        self.assertEqual([], fpt_2.children.keys())
        self.assertEqual(1, fpt_2.count)

        fpt_4 = fpt.children[4]
        self.assertEqual(4, fpt_4.value)
        self.assertEqual([], fpt_4.prefix)
        self.assertEqual([3], fpt_4.children.keys())
        self.assertEqual(1, fpt_4.count)

        fpt_4_3 = fpt_4.children[3]
        self.assertEqual(3, fpt_4_3.value)
        self.assertEqual([4], fpt_4_3.prefix)
        self.assertEqual([], fpt_4_3.children.keys())
        self.assertEqual(1, fpt_4_3.count)

    def test_contains_elements_of_inserted_lists(self):
        fpt = FrequentPatternTree(-1, [])
        for item_list in self.data_set:
            fpt.insert(item_list, [])
        for item_list in self.data_set:
            for item in item_list:
                self.assertTrue(fpt.contains(item))

    def pattern_base_example_getter(self):
        fpt = _generate_frequent_pattern_tree(self.rearranged_data_set)
        desc_list = _get_desc_list_of_frequent_one_items(self.data_set, self.min_sup)
        pattern_base = _construct_pattern_base(desc_list, fpt)

        return pattern_base

    def test_construct_pattern_base(self):
        pattern_base = self.pattern_base_example_getter()
        value = 3
        for node in pattern_base[value]:
            self.assertEqual(node.value, value)
        for i in [1,2,4]:
            if i in pattern_base:
                for node in pattern_base[i]:
                    self.assertNotEqual(node.value, value)

        self.assertEqual([1, [1]], [pattern_base[2][0].count, pattern_base[2][0].prefix])
        self.assertEqual([1, [1,4]], [pattern_base[3][1].count, pattern_base[3][1].prefix])
        self.assertEqual([3, [1]], [pattern_base[4][0].count, pattern_base[4][0].prefix])
        self.assertEqual([1, []], [pattern_base[4][1].count, pattern_base[4][1].prefix])



    def test_convert_pattern_base_to_list_of_conditional_fp_trees(self):
        pattern_base = self.pattern_base_example_getter()

        list_of_cond_fp_trees = _convert_pattern_base_to_list_of_conditional_fp_trees(pattern_base)


        fpt_1 = list_of_cond_fp_trees[0]
        # [value, prefix, count, children]
        fpt_1_expected = [1, [], 1, {}]
        self.assertEqual(fpt_1_expected, [fpt_1.value, fpt_1.prefix, fpt_1.count, fpt_1.children])

        fpt_2 = list_of_cond_fp_trees[1]
        # [value, prefix, count]
        fpt_2_expected = [2, [], 1]
        self.assertEqual(fpt_2_expected, [fpt_2.value, fpt_2.prefix, fpt_2.count])
        fpt_2_1 = fpt_2.children[1]
        fpt_2_1_expected = [1, [2], 2]
        self.assertEqual(fpt_2_1_expected, [fpt_2_1.value, fpt_2_1.prefix, fpt_2_1.count])
        fpt_2_1_4 = fpt_2_1.children[4]
        fpt_2_1_4_expected = [4, [2, 1], 1]
        self.assertEqual(fpt_2_1_4_expected, [fpt_2_1_4.value, fpt_2_1_4.prefix, fpt_2_1_4.count])

        fpt_3 = list_of_cond_fp_trees[2]
        fpt_3_expected = [3, [], 1]
        self.assertEqual(fpt_3_expected, [fpt_3.value, fpt_3.prefix, fpt_3.count])
        fpt_3_1 = fpt_3.children[1]
        fpt_3_1_expected = [1, [3], 2]
        self.assertEqual(fpt_3_1_expected, [fpt_3_1.value, fpt_3_1.prefix, fpt_3_1.count])
        fpt_3_4 = fpt_3.children[4]
        fpt_3_4_expected = [4, [3], 1]
        self.assertEqual(fpt_3_4_expected, [fpt_3_4.value, fpt_3_4.prefix, fpt_3_4.count])

        fpt_4 = list_of_cond_fp_trees[3]
        fpt_4_expected = [4, [], 1]
        self.assertEqual(fpt_4_expected, [fpt_4.value, fpt_4.prefix, fpt_4.count])
        fpt_4_1 = fpt_4.children[1]
        fpt_4_1_expected = [1, [4], 3]
        self.assertEqual(fpt_4_1_expected, [fpt_4_1.value, fpt_4_1.prefix, fpt_4_1.count])

    def is_subset(self, int_list, list_of_int_lists):
        int_tuple = tuple(int_list)
        list_of_int_tuples = []
        for int_list in list_of_int_lists:
            list_of_int_tuples.append(tuple(int_list))
        sub_list = []
        sub_list.append(int_tuple)
        return set(sub_list).issubset(set(list_of_int_tuples))

    def test_mine_fp_tree(self):
        desc_list = _get_desc_list_of_frequent_one_items(self.data_set, self.min_sup)
        pattern_base = self.pattern_base_example_getter()

        list_of_cond_fp_trees = _convert_pattern_base_to_list_of_conditional_fp_trees(pattern_base)

        actual_result_1 = set([i for i in _mine_fp_tree(list_of_cond_fp_trees[0], desc_list) if self.is_subset(list(i), self.rearranged_data_set)])
        self.assertEqual({(1,)}, actual_result_1)

        actual_result_2 = set([i for i in _mine_fp_tree(list_of_cond_fp_trees[1], desc_list) if self.is_subset(list(i), self.rearranged_data_set)])
        self.assertEqual({(2,)}, actual_result_2)

        actual_result_3 = set([i for i in _mine_fp_tree(list_of_cond_fp_trees[2], desc_list) if self.is_subset(list(i), self.rearranged_data_set)])
        self.assertEqual({(3,)}, actual_result_3)

        actual_result_4 = set([i for i in _mine_fp_tree(list_of_cond_fp_trees[3], desc_list) if self.is_subset(list(i), self.rearranged_data_set)])
        self.assertEqual({(4,), (1,), (1,4)}, actual_result_4)

    def test_retrieve(self):
        expected_result = {[(1,), (2,), (4,)]}
        min_sup = 4
        self.assertEqual(expected_result, retrieve(self.data_set, min_sup))

