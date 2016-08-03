class HashTree():
    def __init__(self, k, level):
        self.k = k
        self.children = {}
        self.level = level

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