class HashTree():
    def __init__(self, k, level):
        self.k = k
        self.children = {}
        self.level = level

    def __str__(self):
        output = ""
        if self.level > 0:
            output += "\n"
        tab_width = 3*" "
        output += (self.level * tab_width) + "(k: " + str(self.k) + ", level: " + str(self.level) + ")"
        for key in self.children:
            if isinstance(self.children[key], HashTree):
                output += self.children[key].__str__()
            else:
                output += "\n" + (self.level + 1) * tab_width + "(values: " +  str(key) + ")"
        return output


    def __eq__(self, other):
        if self.k == other.k and self.level == other.level and len(self.children) == len(other.children):
            for i in range(len(self.children.keys())):
                self_key = self.children.keys()[i]
                self_value = self.children.values()[i]
                other_key = self.children.keys()[i]
                other_value = self.children.values()[i]
                if isinstance(self_value, HashTree):
                    if not self_key in other.children or not self_value.__eq__(other_value):
                        return False
                else:
                    if not self_key == other_key:
                        return False

            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def insert(self, tup):
        if self.level == self.k:
            self.children[tup] = 1
        else:
            hash = tup[self.level] % self.k
            if not hash in self.children:
                son = HashTree(self.k, self.level + 1)
                son.insert(tup)
                self.children[hash] = son
            else:
                self.children[hash].insert(tup)

    def contains(self, tup):
        if tup in self.children:
            return True
        elif self.level < self.k:
            hash = tup[self.level] % self.k
            if hash in self.children:
                return self.children[hash].contains(tup)
            else:
                return False
        else:
            return False

    def _helper_get_itemsets_in_transaction(self, original_ta, ta, result):
        if self.level == self.k:
            for c in self.children:
                s = set(c)
                if s.issubset(original_ta):
                    result.update({tuple(c): 1})
            return result
        else:
            for i in range(len(ta)):
                hash = ta[i] % self.k
                if hash in self.children:
                    result.update(
                        self.children[hash]._helper_get_itemsets_in_transaction(original_ta, ta[i + 1:], result))
            return result

    def get_itemsets_in_transaction(self, ta):
        return self._helper_get_itemsets_in_transaction(ta, ta, {})
