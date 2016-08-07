def join(list1, list2):
    """
    Join two integer lists.

    :param list1: (List[int]) list of integers
    :param list2: (List[int]) list of integers

    | Conditions for list1 and list2 to be joined, demonstrated in an example:
    >>> list1 = [1,2,3]
    >>> list2 = [1,2,4]
    >>> len(list1) == len(list2)
    True
    >>> len(list1) > 0
    True
    >>> list1[:-1] == list2[:-1]
    True
    >>> not list1[-1] == list2[-1]
    True

    Returns:
        The Join of the two lists, if join is possible, otherwise the empty list.

    Examples:
        >>> join([1,2,3], [1,2,4])
        [1,2,4]
        >>> join([1,2,3], [1,3,4])
        []
        >>> join([1,2,3], [1,1,4])
        []
        >>> join([785, 43, 0], [785, 43, 1009])
        [785, 43, 0, 1009]
        >>> join([785, 42, 1009], [785, 43, 0])
        [785, 43, 0, 1009]
    """
    
    def equal_length(s1, s2):
        return len(s1) == len(s2)

    def not_empty(s):
        return not s == []

    def common_n_minus_one_length_prefix(s1, s2):
        if s1[:-1] == s2[:-1]:
            return True
        else:
            return False

    def last_not_equal(s1, s2):
        return not s1[-1] == s2[-1]

    if equal_length(list1, list2) \
            and not_empty(list1) \
            and common_n_minus_one_length_prefix(list1, list2) \
            and last_not_equal(list1, list2):

        common = list1[:-1]
        suffixes = [list1[-1], list2[-1]]
        suffixes.sort()
        result = common + suffixes

        return result

    else:

        return []
