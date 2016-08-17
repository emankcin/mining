import unittest

from kdd.fitemset.apriori.hash_tree import HashTree


class HashTreeTest(unittest.TestCase):
    def setUp(self):
        self.ht = HashTree(2, 0)

    def test_hash_tree_string(self):
        self.ht._insert((1, 2))
        self.ht._insert((0, 1))
        self.ht._insert((0, 2))
        self.ht._insert((1, 3))
        self.ht._insert((2, 3))
        expected = ("(k: 2, level: 0)\n"
	                "   (k: 2, level: 1)\n"
		            "      (k: 2, level: 2)\n"
                    "         (values: (0, 2))\n"
		            "      (k: 2, level: 2)\n"
                    "         (values: (0, 1))\n"
                    "         (values: (2, 3))\n"
	                "   (k: 2, level: 1)\n"
		            "      (k: 2, level: 2)\n"
                    "         (values: (1, 2))\n"
		            "      (k: 2, level: 2)\n"
                    "         (values: (1, 3))")
        self.assertEqual(expected, self.ht.__str__())

    def test_hash_tree_equality(self):
        self.ht._insert((1, 2))
        self.ht._insert((0, 1))
        self.ht._insert((0, 2))
        self.ht._insert((1, 3))
        ht_2 = HashTree(self.ht.k, self.ht.level)
        ht_2._insert((1, 2))
        ht_2._insert((0, 1))
        ht_2._insert((0, 2))
        ht_2._insert((1, 3))
        self.assertEqual(self.ht, ht_2)

    def test_contains__inserted_elements(self):
        self.ht._insert((1,2))
        self.ht._insert((0,1))
        self.ht._insert((0,2))
        self.ht._insert((1,3))
        self.assertTrue(self.ht._contains((1,2)))
        self.assertTrue(self.ht._contains((0,1)))
        self.assertTrue(self.ht._contains((0,2)))
        self.assertTrue(self.ht._contains((1,3)))
        self.assertFalse(self.ht._contains((2,3)))

    def test_contains__inserted_elements_with_length_five(self):
        ht_five = HashTree(5, 0)
        ht_five._insert((1, 2, 3, 4, 5))
        self.assertTrue(ht_five._contains((1, 2, 3, 4, 5)))
        self.assertFalse(ht_five._contains((1, 2, 3, 4, 6)))

    def test_get_item_sets_in_transaction(self):
        self.ht._insert((1, 2))
        self.ht._insert((0, 1))
        self.assertEqual({(0, 1): 1, (1, 2): 1}, self.ht._get_item_sets_in_transaction([0, 1, 2]))
        self.assertEqual({(0, 1): 1}, self.ht._get_item_sets_in_transaction([0, 1, 3]))
        self.assertEqual({}, self.ht._get_item_sets_in_transaction([2, 3, 4]))
