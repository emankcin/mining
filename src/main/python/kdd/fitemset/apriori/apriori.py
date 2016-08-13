import numpy as np

from hash_tree import HashTree
from join import join


def _retrieve_frequent_singleton_counts(item_lists, min_sup):
    """
    Counts each item in a list of item lists. Only frequent items are returned.

    An item set is frequent if its count is greater than or equal to the minimum support.

    :param item_lists: list of integer lists
    :param min_sup: minimum support
    :return: dictionary with frequent singletons and their counts
    :rtype: Dict[Tuple[int] : int]

    Example:

    >>> from kdd.fitemset.apriori.apriori import _retrieve_frequent_singleton_counts

    >>> data_set = [[0, 1, 2], [0, 1, 3]]
    >>> min_sup = 2
    >>> _retrieve_frequent_singleton_counts(data_set, min_sup)
    {(0,): 2, (1,): 2}
    """

    counts = {}

    # scan data_set to count singleton item occurrences
    for item_list in item_lists:
        for item in item_list:

            key = (item,)

            if not key in counts:
                counts[key] = 1
            else:
                counts[key] += 1

    # filter out non-frequent items
    counts_copy = counts.copy()
    for key in counts_copy:
        if counts[key] < min_sup:
            counts.pop(key)

    return counts


def _item_lists_self_join(item_lists):
    """
    Example:

    >>> from kdd.fitemset.apriori.apriori import _item_lists_self_join

    >>> item_lists = [[1,2,3], [1,2,4], [1,3,5], [3,4,6], [3,4,8], [3,4,9]]
    >>> _item_lists_self_join(item_lists)
    [[1, 2, 3, 4], [3, 4, 6, 8], [3, 4, 6, 9], [3, 4, 8, 9]]
    """

    join_result = []
    length = len(item_lists)

    for i in range(length):
        for j in range(i + 1, length):
            joined = join(item_lists[i], item_lists[j])
            if joined:
                join_result.append(joined)

    return join_result


def _get_frequent_n_item_tuples_with_counts(data_set, n_item_lists, min_sup):
    """
    Example:

    >>> from kdd.fitemset.apriori.apriori import _get_frequent_n_item_tuples_with_counts

    >>> data_set = [[1,2,3,4,5], [2,3,4,5,6], [3,4,5,6,7]]
    >>> n_item_lists = [[2,3], [3,4]]
    >>> min_sup = 2
    >>> _get_frequent_n_item_tuples_with_counts(data_set, n_item_lists, min_sup)
    {(3, 4): 3, (2, 3): 2}
    """

    k_counts = {}

    # count how often each of the k n_item_lists is subset of a data row
    for row in data_set:
        for n_item_list in n_item_lists:

            contained = set(n_item_list).issubset(set(row))

            if contained:

                n_item_tuple = tuple(n_item_list)

                if not n_item_tuple in k_counts:
                    k_counts[n_item_tuple] = 1
                else:
                    k_counts[n_item_tuple] += 1

    result = {}

    # only put frequent item lists into result
    for n_item_list in n_item_lists:

        n_item_tuple = tuple(n_item_list)

        if n_item_tuple in k_counts and k_counts[n_item_tuple] >= min_sup:

            result[n_item_tuple] = k_counts[n_item_tuple]

    return result

def _get_frequent_n_item_lists(data_set, n_item_lists, min_sup):
    """
        Example:

        >>> from kdd.fitemset.apriori.apriori import _get_frequent_n_item_lists

        >>> data_set = [[1,2,3,4,5], [2,3,4,5,6], [3,4,5,6,7]]
        >>> n_item_lists = [[2,3], [3,4]]
        >>> min_sup = 2
        >>> _get_frequent_n_item_lists(data_set, n_item_lists, min_sup)
        [[3, 4], [2, 3]]
        """
    return [list(tup) for tup in _get_frequent_n_item_tuples_with_counts(data_set, n_item_lists, min_sup).keys()]

def _construct_hash_tree(item_lists):
    if len(item_lists) > 0:
        k = len(item_lists[0])
    else:
        k = 0
    ht = HashTree(k, 0)
    for item_list in item_lists:
        ht.insert(tuple(item_list))
    return ht


def _get_frequent_n_item_tuples_with_counts_by_hash_tree(dataset, hash_tree, min_sup):
    result_dic = {}
    for ta in dataset:
        ta = [int(float(i)) for i in ta]
        ta = list(np.sort(ta, kind='mergesort'))
        tmp = hash_tree.get_itemsets_in_transaction(ta)
        for key in tmp:
            if key in result_dic:
                result_dic[key] = result_dic[key] + tmp[key]
            else:
                result_dic[key] = tmp[key]
    # drop non-frequent item sets
    result_dic = {k: v for k, v in result_dic.iteritems() if v >= min_sup}
    return result_dic


def apriori(data_set, min_sup, with_hash_tree=True):
    """
    The apriori algorithm for retrieving frequent item tuples together with their counts.

    :param data_set: A list of integer-lists (integers usually represent the keys of the items)
    :param min_sup: minimum support, i.e. minimum number of items for them to be considered frequent
    :param with_hash_tree: True is default and means that the hash tree variant is used. False uses simple variant.
    :type with_hash_tree: bool.
    :return: dictionary of frequent item tuples with their counts
    :rtype: Dict[Tuple[int] : int]

    Example:

    >>> from kdd.fitemset.apriori.apriori import apriori

    >>> data_set = [[6], [7], [8], [3,6], [4,7], [5,8], [1,2,3], [7,8,9], [6,7,8,9]]
    >>> min_sup = 3
    >>> apriori(data_set, min_sup)
    {(8,): 4, (6,): 3, (7,): 4}
    >>> min_sup = 2
    >>> apriori(data_set, min_sup)
    {(8,): 4, (3,): 2, (7, 8, 9): 2, (9,): 2, (8, 9): 2, (6,): 3, (7,): 4, (7, 8): 2, (7, 9): 2}
    """
    result =  _retrieve_frequent_singleton_counts(data_set, min_sup)
    k_result = result.copy()

    while True:

        last_k_result = [list(tup) for tup in k_result.keys()]
        new_k_input = _item_lists_self_join(last_k_result)

        if new_k_input == []:
            break
        else:

            if (with_hash_tree):
                hash_tree = _construct_hash_tree(new_k_input)
                k_result = _get_frequent_n_item_tuples_with_counts_by_hash_tree(data_set, hash_tree, min_sup)
            else:
                k_result = _get_frequent_n_item_tuples_with_counts(data_set, new_k_input, min_sup)

            if k_result == {}:
                break
            else:
                result.update(k_result)

    #print "result: "
    #print result
    return result