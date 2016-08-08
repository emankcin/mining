class FrequentPatternTree():
    def __init__(self):
        self.value = -1
        self.prefix = []
        self.count = 0
        self.children = {}
        self.level = 0

    def insert(self, item_list):
        # TODO: work in progress

        if item_list == []:
            pass
        else:
            first_item = item_list[0]
            if self.level == 0:
                if first_item in self.children:
                    self.children[first_item].insert(item_list[1:])
            if self.value == first_item:
                self.count += 1

    def contains(self, item):
        return False


def _get_desc_list_of_frequent_one_items(self, data_set, min_sup):
    return []

def _rearrange_data_set_according_to_one_items(self, data_set, desc_list):
    return []

def _generate_frequent_pattern_tree(self, data_set):
    return FrequentPatternTree()