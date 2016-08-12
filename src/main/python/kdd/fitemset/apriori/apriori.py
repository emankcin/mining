import numpy as np

from hash_tree import HashTree
from join import join


def _retrieve_frequent_singleton_counts(item_lists, min_sup):
    """
    Counts each item in a list of item lists. Non-frequent items are discarded.

    :param item_lists: list of integer lists
    :param min_sup: minimum support
    :return: dictionary with frequent singletons and their counts
    :rtype: Dict[Tuple[int], int]

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


def _get_frequent_n_itemsets(data_set, n_item_lists, min_sup):
    """
    Example:

    >>> from kdd.fitemset.apriori.apriori import _get_frequent_n_itemsets

    >>> data_set = [[1,2,3,4,5], [2,3,4,5,6], [3,4,5,6,7]]
    >>> n_item_lists = [[2,3], [3,4]]
    >>> min_sup = 2
    >>> _get_frequent_n_itemsets(data_set, n_item_lists, min_sup)
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


def _construct_hash_tree(dic):
    if len(dic.values()) > 0:
        k = len(dic.values()[0])
    else:
        k = 0
    ht = HashTree(k, 0)
    for i in dic.values():
        ht.insert(tuple(i))
    return ht


def _get_f_n_itemsets_w_hashtree(dataset, hash_tree, min_sup):
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


def apriori(dataset, max_items, min_sup, with_hash_tree=True):
    """
    The apriori algorithm for retrieving frequent item sets.

    :param dataset: A list of integer-lists (integers usually represent the keys of the items)
    :param max_items: maximum number of different items
    :param min_sup: minimum support, i.e. minimum number of items for them to be considered frequent
    :param with_hash_tree: True is default and means that the hash tree variant is used. False uses simple variant.
    :type with_hash_tree: bool.
    """
    result = {}

    k_result = _retrieve_frequent_singleton_counts(dataset, min_sup)

    result.update(k_result)

    while True:
        k_result = [list(tup) for tup in k_result.keys()]
        k_result = _item_lists_self_join(k_result)
        #k_result = dict(zip([i for i in range(len(k_result))], k_result))

        if k_result == []:
            break
        if (with_hash_tree):
            hash_tree = _construct_hash_tree(k_result)
            k_result = _get_f_n_itemsets_w_hashtree(dataset, hash_tree, min_sup)
        else:
            k_result = _get_frequent_n_itemsets(dataset, k_result, min_sup)
        if k_result == {}:
            break
        else:
            result.update(k_result)

    #print "result: "
    #print result
    return result