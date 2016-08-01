from join import join


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
    return set([i for i in counts.keys()])


def itemsets_self_join(list_of_itemsets):
    k_result = {}
    c = 0
    ci = 0
    for i in list_of_itemsets:
        ci += 1
        cj = 0
        for j in list_of_itemsets:
            cj += 1
            if ci >= cj:
                continue
            joined = join(i, j)
            if not joined:
                continue
            else:
                k_result[c] = joined
                c += 1
    return k_result

# parameter types: list of lists, dictionary, integer
def get_frequent_n_itemsets(dataset, current_list, min_sup):
    k_counts = {}
    for row in dataset:
        row = [int(float(i)) for i in row]
        for key in current_list:
            contained = set(current_list[key]).issubset(set(row))
            if not contained:
                continue
            else:
                if not tuple(current_list[key]) in k_counts:
                    k_counts[tuple(current_list[key])] = 1
                else:
                    k_counts[tuple(current_list[key])] += 1
    result = {}
    for i in range(len(current_list)):
        if tuple(current_list[i]) in k_counts and k_counts[tuple(current_list[i])] >= min_sup:
            result[tuple(current_list[i])] = k_counts[tuple(current_list[i])]
    return result


def apriori_without_hashsets(dataset, max_items, min_sup):
    counts = get_frequent_one_itemsets(dataset, max_items, min_sup)

    result = {}
    end_result = {}
    for i in counts:
        result[i[0]] = list(i)
        end_result[i] = list(i)

    while True:
        # join list with itself
        k_result = itemsets_self_join(result)
        k_result = get_frequent_n_itemsets(dataset, k_result, min_sup)
        result = k_result
        if k_result == {}:
            break
        else:
            print "New iteration"
            end_result.update(k_result)

    print "Frequenet itemsets:"
    end_result = set(end_result)
    print end_result
    return set(end_result)
