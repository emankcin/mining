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


def apriori_without_hashsets(dataset, max_items, min_sup):

    counts = get_frequent_one_itemsets(dataset, max_items, min_sup)

    result = {}
    end_result = {}
    for i in counts:
        result[i[0]] = list(i)
        end_result[i] = list(i)

    cont = True
    while cont:
        cont = False
        # join list with itself
        k_result = {}
        c = 0
        print "New iteration"
        ci = 0
        resl = [[i] for i in list(result)]
        for i in resl:
            ci += 1
            cj = 0
            for j in resl:
                cj += 1
                if ci >= cj:
                    continue
                joined = join(i, j)
                if not joined:
                    continue
                else:
                    k_result[c] = joined
                    c += 1
        k_counts = {}
        for row in dataset:
            row = [int(float(i)) for i in row]
            for key in k_result:
                contained = set(k_result[key]).issubset(set(row))
                if not contained:
                    continue
                else:
                    if not tuple(k_result[key]) in k_counts:
                        k_counts[tuple(k_result[key])] = 1
                    else:
                        k_counts[tuple(k_result[key])] += 1
        cont = False
        result = {}
        for i in range(len(k_result)):
            if tuple(k_result[i]) in k_counts and k_counts[tuple(k_result[i])] >= min_sup:
                end_result[tuple(k_result[i])] = k_counts[tuple(k_result[i])]
                result[tuple(k_result[i])] = k_counts[tuple(k_result[i])]
                cont = True
        print end_result
        if not cont:
            break

    print "Frequenet itemsets:"
    end_result = set(end_result)
    print end_result
    return set(end_result)