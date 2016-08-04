import unittest

from fitemset.apriori.hash_tree import HashTree


class HashTreeTest(unittest.TestCase):
    def setUp(self):
        self.ht = HashTree(2, 0)

    def test_contains_inserted_elements(self):
        self.ht.insert((1,2))
        self.ht.insert((0,1))
        self.ht.insert((0,2))
        self.ht.insert((1,3))
        self.assertTrue(self.ht.contains((1,2)))
        self.assertTrue(self.ht.contains((0,1)))
        self.assertTrue(self.ht.contains((0,2)))
        self.assertTrue(self.ht.contains((1,3)))
        self.assertFalse(self.ht.contains((2,3)))

    def test_contains_inserted_elements_with_length_five(self):
        ht_five = HashTree(5, 0)
        ht_five.insert((1, 2, 3, 4, 5))
        self.assertTrue(ht_five.contains((1, 2, 3, 4, 5)))
        self.assertFalse(ht_five.contains((1, 2, 3, 4, 6)))

    def test_get_item_sets_in_transaction(self):
        self.ht.insert((1, 2))
        self.ht.insert((0, 1))
        self.assertEqual({(0, 1): 1, (1, 2): 1}, self.ht.get_itemsets_in_transaction([0, 1, 2]))
        self.assertEqual({(0, 1): 1}, self.ht.get_itemsets_in_transaction([0, 1, 3]))
        self.assertEqual({}, self.ht.get_itemsets_in_transaction([2, 3, 4]))
