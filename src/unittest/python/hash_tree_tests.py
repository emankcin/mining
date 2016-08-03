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