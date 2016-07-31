# join([1,2,3], [1,2,4]) = [1,2,3,4]
# join([1,8,9], [1,5,6]) = []
def join(set1, set2):

	def equal_length(s1, s2):
		return len(s1) == len(s2)

	def not_empty(s):
		return not s == []

	def common_n_minus_one_length_prefix(s1, s2):
		if s1[:-1] == s2[:-1]:
			return True
		else:
			return False

	def last_not_equal(set1, set2):
		return not set1[-1] == set2[-1]

	
	if equal_length(set1, set2) \
		and not_empty(set1) \
		and common_n_minus_one_length_prefix(set1, set2) \
		and last_not_equal(set1, set2):
		
		common_set = set1[:-1]
		suffixes = [set1[-1], set2[-1]]
		suffixes.sort()
		result = common_set + suffixes
		
		return result
	
	else:
	
		return []