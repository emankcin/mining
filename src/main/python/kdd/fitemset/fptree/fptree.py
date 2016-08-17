import numpy as np
from itertools import combinations


class FrequentPatternTree():
    def __init__(self, value, prefix):
        self.value = value
        self.prefix = prefix
        self.count = 1
        self.children = {}

    def _str(self, level):
        output = ""
        if level > 0:
            output += "\n"
        output += (level * "   ") + str(self.value) + ":" + str(self.count)
        for child in self.children.values():
            output += child._str(level + 1)
        return output

    def __str__(self):
        return self._str(0)

    def __eq__(self, other):
        if self.value == other.value and self.prefix == other.prefix and self.count == other.count and len(
                self.children) == len(other.children):
            for key in self.children:
                if not key in other.children or not self.children[key].__eq__(other.children[key]):
                    return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def insert(self, item_list, prefix):
        if item_list == []:
            pass
        else:
            first_item = item_list[0]
            if not first_item in self.children:
                self.children[first_item] = FrequentPatternTree(first_item, prefix)
            else:
                self.children[first_item].count += 1
            next_prefix = prefix[:]
            next_prefix.append(first_item)
            self.children[first_item].insert(item_list[1:], next_prefix)

    def contains(self, item):
        if self.value == item:
            return True
        else:
            for key in self.children:
                if True == self.children[key].contains(item):
                    return True
            return False

    def get_all_nodes_with_value(self, value):
        nodes = []
        return self.get_all_nodes_with_values_helper(value, nodes)

    def get_all_nodes_with_values_helper(self, value, nodes):
        if self.value == value:
            nodes.append(self)
        else:
            for child in self.children:
                nodes = self.children[child].get_all_nodes_with_values_helper(value, nodes)
        return nodes

    def is_frequent_single_path(self, min_sup):
        if len(self.children) > 1:
            return []
        elif len(self.children) == 0 or (self.count < min_sup and not self.prefix == []):
            result = self.prefix[:]
            if self.count >= min_sup or self.prefix == []:
                result.append(self.value)
            return result
        else:
            return self.children.values()[0].is_frequent_single_path(min_sup)

    def retrieve_frequent_item_sets_of_single_path(self, min_sup):
        result = set()
        path = self.is_frequent_single_path(min_sup)
        if not path:
            return set()
        else:
            for L in range(1, len(path) + 1):
                result = result.union(set([tuple(sorted(i)) for i in list(combinations(path, L))]))
        return result

    def retrieve_frequent_item_sets_of_multi_path(self, min_sup):
        return set()

def _get_desc_list_of_frequent_one_items(data_set, min_sup):
    items = {}
    for item_list in data_set:
        for item in item_list:
            if item in items:
                items[item] += 1
            else:
                items[item] = 1
    frequent_items = {k: v for k, v in items.iteritems() if v >= min_sup}
    desc_sorted_frequent_items = sorted(frequent_items, key=frequent_items.get, reverse=True)

    return desc_sorted_frequent_items


def _rearrange_data_set_according_to_one_items(data_set, desc_list):
    rearranged = []

    for item_list in data_set:
        tmp = [i for i in item_list if i in desc_list]
        np_tmp = np.array(tmp)

        tmp_desc = [i for i in desc_list if i in tmp]
        np_tmp_desc = np.array(tmp_desc)

        ind = np_tmp_desc.argsort()
        desc_count_sorted_list = np_tmp[ind].tolist()

        rearranged.append(desc_count_sorted_list)

    return rearranged


def _generate_frequent_pattern_tree(data_set):
    fpt = FrequentPatternTree(-1, [])
    for item_list in data_set:
        fpt.insert(item_list, [])
    return fpt


def _construct_pattern_base(item_list, fp_tree):
    pattern_base = {}
    for item in item_list:
        if fp_tree.contains(item):
            pattern_base[item] = fp_tree.get_all_nodes_with_value(item)
    return pattern_base


def _convert_pattern_base_to_list_of_conditional_fp_trees(pattern_base):
    result_list = []
    for key in pattern_base:
        conditional_fpt = FrequentPatternTree(key, [])
        tree_list = pattern_base[key]
        for tree in tree_list:
            for i in range(tree.count):
                conditional_fpt.insert(tree.prefix, [key])
        result_list.append(conditional_fpt)
    return result_list

def is_subset(self, int_list, list_of_int_lists):
    int_tuple = tuple(int_list)
    list_of_int_tuples = []
    for int_list in list_of_int_lists:
        list_of_int_tuples.append(tuple(int_list))
    sub_list = []
    sub_list.append(int_tuple)
    return set(sub_list).issubset(set(list_of_int_tuples))

def _mine_fp_tree(fp_tree, desc_list, min_sup):
    result = set()
    is_single_path = fp_tree.is_frequent_single_path(min_sup)
    if is_single_path:
        result = fp_tree.retrieve_frequent_item_sets_of_single_path(min_sup)
    else:
        pattern_base = _construct_pattern_base(desc_list, fp_tree)
        list_of_trees = _convert_pattern_base_to_list_of_conditional_fp_trees(pattern_base)

        for tree in list_of_trees:
            tree_with_root = FrequentPatternTree(-1, [])
            tree_with_root.children[tree.value] = tree
            is_single_path = tree_with_root.is_frequent_single_path(min_sup)
            if is_single_path:
                res = tree_with_root.retrieve_frequent_item_sets_of_single_path(min_sup)
            else:
                res = tree_with_root.retrieve_frequent_item_sets_of_multi_path(min_sup)
            result = result.union(res)

    return result


def retrieve(data_set, min_sup):
    desc_list = _get_desc_list_of_frequent_one_items(data_set, min_sup)
    rearranged = _rearrange_data_set_according_to_one_items(data_set, desc_list)
    fpt = _generate_frequent_pattern_tree(rearranged)
    result = _mine_fp_tree(fpt, desc_list, min_sup)
    result = list(result)
    result.sort()

    return result
