import time
from pandas import read_csv

from apriori.apriori import apriori
from fptree.fp_tree_algorithm import retrieve_frequent_item_tuples


def convert_receipts(raw_dataset):
    dataset = []
    for itemset in raw_dataset:
        tmp = itemset.split(',')
        tmp.pop(0)
        tmp = [int(float(s)) for s in tmp]
        dataset.append(tmp)
    return dataset


def load_receipts_csv(path):
    raw_dataset = read_csv(path, "r", header=None)[0]
    dataset = convert_receipts(raw_dataset)
    return dataset


def main():
    receipts = "../../../resources/receipts.csv"
    #description = "../../../resources/item_description.csv"

    dataset = load_receipts_csv(receipts)
    dataset = dataset[:500]

    #item_description = read_csv(description, "r", header=None, delimiter=",", index_col=0, skiprows=1)

    min_sup = 3

    t1 = time.time()
    sets1 = apriori(dataset, min_sup, with_hash_tree=False)
    t1 = time.time() - t1
    print "apriori without hash tree: ", sets1
    print "(as sorted list) apriori without hash tree: "
    print sorted(sets1.keys())

    t2 = time.time()
    sets2 = apriori(dataset, min_sup, with_hash_tree=True)
    t2 = time.time() - t2
    print "apriori with hash tree: ", sets2
    print "(as sorted list:) apriori with hash tree: "
    print sorted(sets2.keys())
    print "comparison of apriori algorithm variants:"
    print "hash tree variant needed ", (t2 / t1) * 100, "% of the time of the variant without a hash tree."

    print "apriori variants have same result: ", sets1 == sets2

    t3 = time.time()
    sets3 = retrieve_frequent_item_tuples(dataset, min_sup)
    t3 = time.time() - t3
    print "(as sorted list:) frequent pattern tree algorithm: "
    print sets3
    print "comparison of hash tree apriori with fp tree algorithm: "
    print "fp tree algorithm needed ", (t3 / t1) * 100, "% of the time of the apriori variant without a hash tree"

    print "apriori variants and fp tree algorithm have same result: ", sets1 == sets2 and sorted(sets2.keys()) == sets3

if __name__ == "__main__":
    main()