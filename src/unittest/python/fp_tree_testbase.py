import unittest


class FPTreeTestBase(unittest.TestCase):
    def setUp(self):
        self.data_set = [[1], [2],
                         [1, 2], [1, 3], [1, 4], [3, 4],
                         [1, 2, 4], [1, 3, 4]]
        self.min_sup = 3
        self.rearranged_data_set = [[1], [2],
                                    [1, 2], [1, 3], [1, 4], [4, 3],
                                    [1, 4, 2], [1, 4, 3]]
        self.result = {(1,), (2,), (3,), (4,), (1, 4)}
