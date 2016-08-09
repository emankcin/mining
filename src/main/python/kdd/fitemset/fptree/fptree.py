class FrequentPatternTree():
    def __init__(self, value):
        self.value = value
        self.count = 0
        self.children = {}

    def insert(self, item_list):
        if item_list == []:
            pass
        else:
            first_item = item_list[0]
            if not first_item in self.children:
                self.children[first_item] = FrequentPatternTree(first_item)
            self.count += 1
            self.children[first_item].insert(item_list[1:])

    def contains(self, item):
        if self.value == item:
            return True
        else:
            for key in self.children:
                if True == self.children[key].contains(item):
                    return True
            return False


def _get_desc_list_of_frequent_one_items(self, data_set, min_sup):
    return []

def _rearrange_data_set_according_to_one_items(self, data_set, desc_list):
    return []

def _generate_frequent_pattern_tree(self, data_set):
    fpt = FrequentPatternTree(-1)
    for item_list in data_set:
        fpt.insert(item_list)
    return fpt