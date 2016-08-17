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

    def _insert(self, item_list, prefix):
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
            self.children[first_item]._insert(item_list[1:], next_prefix)

    def _contains(self, item):
        if self.value == item:
            return True
        else:
            for key in self.children:
                if True == self.children[key]._contains(item):
                    return True
            return False

    def _get_all_nodes_with_value(self, value):
        nodes = []
        return self._get_all_nodes_with_values_helper(value, nodes)

    def _get_all_nodes_with_values_helper(self, value, nodes):
        if self.value == value:
            nodes.append(self)
        else:
            for child in self.children:
                nodes = self.children[child]._get_all_nodes_with_values_helper(value, nodes)
        return nodes

    def _is_frequent_single_path(self, min_sup):
        if len(self.children) > 1:
            return []
        elif len(self.children) == 0 or (self.count < min_sup and not self.prefix == []):
            result = self.prefix[:]
            if self.count >= min_sup or self.prefix == []:
                result.append(self.value)
            return result
        else:
            return self.children.values()[0]._is_frequent_single_path(min_sup)

    def _retrieve_frequent_item_sets_of_single_path(self, min_sup):
        result = set()
        path = self._is_frequent_single_path(min_sup)
        if not path:
            return set()
        else:
            for L in range(1, len(path) + 1):
                result = result.union(set([tuple(sorted(i)) for i in list(combinations(path, L))]))
        return result
