import unittest
from fitemset.apriori.join import join

class JoinTestCase(unittest.TestCase):

	def test_join_common_case(self):
		self.assertEqual([1,2,3,4], join([1,2,3], [1,2,4]))

	def test_join_with_differing_prefix(self):
		self.assertEqual([], join([1,2,3], [1,1,1]))

	def test_join_empty_set(self):
		self.assertEqual([], join([], []))

	def test_join_differing_length(self):
		self.assertEqual([], join([1,2,3], [1,2,4,5]))

	def test_join_sets_with_length_one(self):
		self.assertEqual([1,2], join([1], [2]))

#if __name__ == "__main__":
#	suite = unittest.TestLoader().loadTestsFromTestCase(JoinTestCase)
#	unittest.TextTestRunner(verbosity=1).run(suite)