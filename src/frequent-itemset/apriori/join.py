import unittest

# join([1,2,3], [1,2,4]) = [1,2,3,4]
# join([1,8,9], [1,5,6]) = []
def join(set1, set2):

	def equal_length(s1, s2):
		return len(s1) == len(s2)

	def not_empty(s):
		return not s == []

	def common_prefix(s1, s2):
			if s1[:-1] == s2[:-1]:
				return True
			else:
				return False

	if equal_length(set1, set2) and not_empty(set1)	and	common_prefix(set1, set2):
		common_set = set1[:-1]
		suffixes = [set1[-1], set2[-1]]
		if(suffixes[0] == suffixes[1]):
			return []
		else:
			suffixes.sort()
			common_set.extend(suffixes)
			return common_set
	else:
		return []

class JoinTestCase(unittest.TestCase):

	def test_join_common_case(self):
		actual = join([1,2,3], [1,2,4])
		expected = [1,2,3,4]
		self.assertEqual(expected, actual)

	def test_join_with_differing_prefix(self):
		actual = join([1,2,3], [1,1,1])
		expected = []
		self.assertEqual(expected, actual)

	def test_join_empty_set(self):
		actual = join([], [])
		expected = []
		self.assertEqual(expected, actual)

	def test_join_differing_length(self):
		actual = join([1,2,3], [1,2,4,5])
		expected = []
		self.assertEqual(expected, actual)

	def test_join_sets_with_length_one(self):
		actual = join([1], [2])
		expected = [1,2]
		self.assertEqual(expected, actual)

suite = unittest.TestLoader().loadTestsFromTestCase(JoinTestCase)
unittest.TextTestRunner(verbosity=1).run(suite)