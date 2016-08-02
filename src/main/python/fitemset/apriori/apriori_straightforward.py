from join import join
import numpy as np


def get_frequent_one_itemsets(dataset, max_items, min_sup):
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

def itemsets_self_join(dic):
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

def get_frequent_n_itemsets(dataset, current_dic, min_sup):
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

def construct_hash_tree(dic):
    n = len(dic.keys()[0])
    ret_dic = {}
    str = ''
    for i in dic.keys():
        for j in i:
            str += j % n + ','
        if not str in ret_dic:
            ret_dic[str] = {}
        ret_dic[str][i] = n
    return ret_dic

def get_f_n_itemsets_w_hashtree(dataset, hash_tree, min_sup):
    result_dic = {}
    k = hash_tree.values()[0]
    for ta in dataset:
        ta = list(np.sort(ta, kind='mergesort'))
        for i in range(len(ta)-k+1):
            str = ''
            hash = ta[i] % k
            str += hash + ','
            for j in range(i+1, len(ta)-k+i+1):
                hash = ta[j] % k
                str += hash + ','
            if str in hash_tree:
                if hash_tree[str] == k:
                    if hash_tree[str] in result_dic:
                        result_dic[hash_tree[str]] += 1
                    else:
                        result_dic[hash_tree[str]] = 1
    return result_dic


def apriori_without_hashsets(dataset, max_items, min_sup):

    result = {}

    k_result = get_frequent_one_itemsets(dataset, max_items, min_sup)

    result.update(k_result)

    while True:
        k_result = itemsets_self_join(k_result)
        #hash_tree = construct_hash_tree(k_result)
        #k_result = get_f_n_itemsets_w_hashtree(dataset, hash_tree, min_sup)
        k_result = get_frequent_n_itemsets(dataset, k_result, min_sup)
        if k_result == {}:
            break
        else:
            result.update(k_result)

    return result