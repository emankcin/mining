import numpy as np

from hash_tree import HashTree
from join import join


def get_singleton_frequent_item_sets(data_set, max_items, min_sup):
    """
    Example:

    >>> from kdd.fitemset.apriori.apriori import get_singleton_frequent_item_sets

    >>> data_set = [['0', '1', '2'], ['0', '1', '3']]
    >>> max_items = 4
    >>> min_sup = 2
    >>> get_singleton_frequent_item_sets(data_set, max_items, min_sup)
    {(0,): 2, (1,): 2}
    """

    # initialize counts
    counts = {(key,): 0 for key in range(max_items)}

    # scan data_set to count singleton item occurrences
    for item_list in data_set:
        for item in item_list:
            key = int(float(item))
            counts[(key,)] += 1

    # filter out non-frequent items
    for key in counts.copy():
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


def _get_frequent_n_itemsets(dataset, current_dic, min_sup):
    k_counts = {}
    for row in dataset:
        row = [int(float(i)) for i in row]
        for key in current_dic:
            contained = set(current_dic[key]).issubset(set(row))
            if not contained:
                continue
            else:
                if not tuple(current_dic[key]) in k_counts:
                    k_counts[tuple(current_dic[key])] = 1
                else:
                    k_counts[tuple(current_dic[key])] += 1
    result = {}
    for i in range(len(current_dic)):
        if tuple(current_dic[i]) in k_counts and k_counts[tuple(current_dic[i])] >= min_sup:
            result[tuple(current_dic[i])] = k_counts[tuple(current_dic[i])]
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

    k_result = get_singleton_frequent_item_sets(dataset, max_items, min_sup)

    result.update(k_result)

    while True:
        k_result = [list(tup) for tup in k_result.keys()]
        k_result = _item_lists_self_join(k_result)
        k_result = dict(zip([i for i in range(len(k_result))], k_result))

        if k_result == {}:
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