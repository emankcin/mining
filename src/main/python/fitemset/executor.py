from pandas import read_csv

from apriori.apriori import apriori


def convert_receipts(raw_dataset):
    dataset = []
    for itemset in raw_dataset:
        tmp = itemset.split(',')
        tmp.pop(0)
        dataset.append(tmp)
    return dataset


def load_receipts_csv(path):
    raw_dataset = read_csv(path, "r", header=None)[0]
    dataset = convert_receipts(raw_dataset)
    return dataset


def main():
    receipts = "../../resources/receipts.csv"
    description = "../../resources/item_description.csv"

    dataset = load_receipts_csv(receipts)
    dataset = dataset[:5000]

    item_description = read_csv(description, "r", header=None, delimiter=",", index_col=0, skiprows=1)

    maxItems = len(item_description.index)
    min_sup = 5

    import time
    t1 = time.time()
    apriori(dataset, maxItems, min_sup, with_hash_tree=False)
    t1 = time.time() - t1
    # print "without hash tree: ", t

    t2 = time.time()
    apriori(dataset, maxItems, min_sup, with_hash_tree=True)
    t2 = time.time() - t2
    # print "with hash tree: ", t
    print "comparison of apriori algorithm variants:"
    print "hash tree variant needed ", (t2 / t1) * 100, "% of the time of the variant without a hash tree."


if __name__ == "__main__":
    main()