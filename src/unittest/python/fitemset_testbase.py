import unittest


class FItemsetTestBase(unittest.TestCase):

    def setUp(self):
        self.data_set = [[0, 1, 2, 3],
                         [0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3],
                         [1, 2], [1, 3], [2, 3],
                         [3]]
        self.n = 4
        # resulting frequent item sets for different values of min_sup:
        self.f_two_item_sets = {(1, 2): 4, (0, 1): 3, (1, 3): 4, (2, 3): 4, (0, 3): 3, (0, 2): 3,
                                (0,): 4, (1,): 6, (2,): 6, (3,): 7}
        self.f_three_item_sets = {(1, 2): 4, (0, 1): 3, (1, 3): 4, (2, 3): 4, (0, 3): 3, (0, 2): 3,
                                  (0,): 4, (1,): 6, (2,): 6, (3,): 7}
        self.f_four_item_sets = {(1, 2): 4, (0,): 4, (2, 3): 4, (1,): 6, (1, 3): 4, (2,): 6, (3,): 7}
        self.f_five_item_sets = {(2,): 6, (3,): 7, (1,): 6}
        self.f_six_item_sets = {(2,): 6, (3,): 7, (1,): 6}
        self.f_seven_item_sets = {(3,): 7}
