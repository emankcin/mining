import numpy as np

class FrequentPatternTree():
    def __init__(self, value, prefix):
        self.value = value
        self.prefix = prefix
        self.count = 0
        self.children = {}

    def insert(self, item_list, prefix):
        if item_list == []:
            pass
        else:
            first_item = item_list[0]
            if not first_item in self.children:
                self.children[first_item] = FrequentPatternTree(first_item, prefix)
            self.count += 1
            next_prefix = self.prefix + first_item
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
                self.get_all_nodes_with_values_helper(value, nodes)
        return nodes

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

def _store_header_table_references(item_list, fp_tree):
    header_table = {}
    for item in item_list:
        if fp_tree.contains(item):
            header_table[item] = fp_tree.get_all_nodes_with_value(item)
    return header_table

