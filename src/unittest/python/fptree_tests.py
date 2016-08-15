from fitemset_testbase import FItemsetTestBase
from kdd.fitemset.fptree.fptree import FrequentPatternTree, _get_desc_list_of_frequent_one_items, _rearrange_data_set_according_to_one_items, _generate_frequent_pattern_tree, _construct_pattern_base, _convert_pattern_base_to_list_of_conditional_fp_trees, _mine_fp_tree

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
        fpt = _generate_frequent_pattern_tree(rearranged_data_set)

        for item_list in rearranged_data_set:
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

    def test_construct_pattern_base(self):
        min_sup = 3
        rearranged_data_set = [[1], [2],
                               [1, 2], [1, 3], [1, 4], [4, 3],
                               [1, 4, 2], [1, 4, 3]]
        fpt = _generate_frequent_pattern_tree(rearranged_data_set)
        desc_list = _get_desc_list_of_frequent_one_items(self.data_set, min_sup)
        pattern_base = _construct_pattern_base(desc_list, fpt)

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
        min_sup = 3
        rearranged_data_set = [[1], [2],
                               [1, 2], [1, 3], [1, 4], [4, 3],
                               [1, 4, 2], [1, 4, 3]]
        fpt = _generate_frequent_pattern_tree(rearranged_data_set)
        desc_list = _get_desc_list_of_frequent_one_items(self.data_set, min_sup)
        pattern_base = _construct_pattern_base(desc_list, fpt)

        list_of_cond_fp_trees = _convert_pattern_base_to_list_of_conditional_fp_trees(pattern_base)
        for tree in list_of_cond_fp_trees:
            print(tree.value)
            print(tree.prefix)
            print(tree.count)
            print(tree.children)

    def test_mine_fp_tree(self):
        min_sup = 3
        rearranged_data_set = [[1], [2],
                               [1, 2], [1, 3], [1, 4], [4, 3],
                               [1, 4, 2], [1, 4, 3]]
        fpt = _generate_frequent_pattern_tree(rearranged_data_set)
        desc_list = _get_desc_list_of_frequent_one_items(self.data_set, min_sup)
        pattern_base = _construct_pattern_base(desc_list, fpt)

        list_of_cond_fp_trees = _convert_pattern_base_to_list_of_conditional_fp_trees(pattern_base)
        print(desc_list)
        print(list_of_cond_fp_trees[1].value)
        print(list_of_cond_fp_trees[1].prefix)
        print(list_of_cond_fp_trees[1].count)
        print(list_of_cond_fp_trees[1].children)
        print(list_of_cond_fp_trees[1].children[1].count)
        print(_mine_fp_tree(list_of_cond_fp_trees[1], desc_list))
