class HashTree():
    def __init__(self, k, level):
        self.k = k
        self.data = []
        self.children = []
        self.level = level

    def insert(self, tup):
        if self.level == self.k:
            self.children.append(tup)
        else:
            hash = tup[self.level] % self.k
            self.children[hash].insert(self, tup)