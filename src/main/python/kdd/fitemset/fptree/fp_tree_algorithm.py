from kdd.fitemset.fptree.fp_tree import FrequentPatternTree


def _get_desc_list_of_frequent_one_items(data_set, min_sup):
    items = {}
    for item_list in data_set:
        for item in item_list:
            if item in items:
                items[item] += 1
            else:
                items[item] = 1
    frequent_items = {k: v for k, v in items.iteritems() if v >= min_sup}
    desc_sorted_frequent_items = sorted(frequent_items, key=frequent_items.get, reverse=True)

    return desc_sorted_frequent_items


def _rearrange_data_set_according_to_one_items(data_set, desc_list):
    rearranged = []

    for item_list in data_set:
        new_item_list = []
        for i in desc_list:
            if i in item_list:
                new_item_list.append(i)
        if new_item_list:
            rearranged.append(new_item_list)

    return rearranged


def _generate_frequent_pattern_tree(data_set):
    fpt = FrequentPatternTree(-1, [])
    for item_list in data_set:
        fpt._insert(item_list, [])
    return fpt


def _construct_pattern_base(item_list, fp_tree):
    pattern_base = {}
    for item in item_list:
        if fp_tree._contains(item):
            pattern_base[item] = fp_tree._get_all_nodes_with_value(item)
    return pattern_base


def _convert_pattern_base_to_list_of_conditional_fp_trees(pattern_base):
    result_list = []
    for key in pattern_base:
        conditional_fpt = FrequentPatternTree(key, [])
        tree_list = pattern_base[key]
        for tree in tree_list:
            for i in range(tree.count):
                conditional_fpt._insert(tree.prefix, [key])
        result_list.append(conditional_fpt)
    return result_list


def _mine_fp_tree(fp_tree, desc_list, min_sup):
    result = set()
    is_single_path = fp_tree._is_frequent_single_path(min_sup)
    if is_single_path:
        result = fp_tree._retrieve_frequent_item_sets_of_single_path(min_sup)
    else:
        pattern_base = _construct_pattern_base(desc_list, fp_tree)
        list_of_trees = _convert_pattern_base_to_list_of_conditional_fp_trees(pattern_base)

        for tree in list_of_trees:
            tree_with_root = FrequentPatternTree(-1, [])
            tree_with_root.children[tree.value] = tree
            is_single_path = tree_with_root._is_frequent_single_path(min_sup)
            if is_single_path:
                res = tree_with_root._retrieve_frequent_item_sets_of_single_path(min_sup)
            else:
                res = _mine_fp_tree(tree_with_root, desc_list, min_sup)
            result = result.union(res)

    if (-1,) in result:
        result.remove((-1,))

    return result


def retrieve_frequent_item_tuples(data_set, min_sup):
    """
    Retrieve the frequent item tuples of a data set according to a minimum support.

    :param data_set: list of integer lists
    :param min_sup: the minimum amount for an item to be considered frequent
    :return: a sorted list of item tuples that are frequent in the data set
    :rtype: List[Tuple[int]]

    Example:
    >>> from kdd.fitemset.fptree.fp_tree_algorithm import retrieve_frequent_item_tuples

    >>> data_set = [[1,2], [1,3], [1,4], [2], [2,3,4], (3,4)]
    >>> min_sup = 2
    >>> retrieve_frequent_item_tuples(data_set, min_sup)
    [(1,), (2,), (3,), (3, 4), (4,)]
    """
    desc_list = _get_desc_list_of_frequent_one_items(data_set, min_sup)
    rearranged = _rearrange_data_set_according_to_one_items(data_set, desc_list)
    fpt = _generate_frequent_pattern_tree(rearranged)
    result = _mine_fp_tree(fpt, desc_list, min_sup)
    result = sorted(list(result))

    return result
