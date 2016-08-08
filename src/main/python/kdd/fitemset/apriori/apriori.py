import numpy as np

from hash_tree import HashTree
from join import join


def _get_frequent_one_itemsets(dataset, max_items, min_sup):
    counts = {}
    for i in range(max_items):
        counts[(i,)] = 0
    # scan dataset to count single item occurrences
    for row in dataset:
        for col in row:
            key = int(float(col))
            counts[(key,)] += 1
    for i in range(len(counts)):
        if counts[(i,)] < min_sup:
            counts.pop((i,))
    return counts


def _itemsets_self_join(dic):
    k_result = {}
    counter = 0
    ci = 0
    for i in dic:
        ci += 1
        cj = 0
        for j in dic:
            cj += 1
            if ci >= cj:
                continue
            joined = join(list(i), list(j))
            if not joined:
                continue
            else:
                k_result[counter] = joined
                counter += 1
    return k_result


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
    k = len(dic.values()[0])
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

    k_result = _get_frequent_one_itemsets(dataset, max_items, min_sup)

    result.update(k_result)

    while True:
        k_result = _itemsets_self_join(k_result)

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

    print "result: "
    print result
    return result