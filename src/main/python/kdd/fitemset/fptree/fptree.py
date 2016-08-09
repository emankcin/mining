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
    return []

def _rearrange_data_set_according_to_one_items(data_set, desc_list):
    return []

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

