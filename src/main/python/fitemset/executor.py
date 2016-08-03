import pandas as pd

from fitemset.apriori.apriori_straightforward import apriori_without_hashsets


def convert_receipts(raw_dataset):
    dataset = []
    for itemset in raw_dataset:
        tmp = itemset.split(',')
        tmp.pop(0)
        dataset.append(tmp)
    return dataset

def load_receipts_csv(path):
    raw_dataset = pd.read_csv(path, "r", header=None)[0]
    dataset = convert_receipts(raw_dataset)
    return dataset

def main():
    receipts = "../../resources/receipts.csv"
    description = "../../resources/item_description.csv"

    #    if sys.argv[1]:
    #       receipts = sys.argv[1]
    #  if sys.argv[2]:
    #     description = sys.argv[2]

    dataset = load_receipts_csv(receipts)
    dataset = dataset[:30]

    item_description = pd.read_csv(description, "r", header=None, delimiter=",", index_col=0, skiprows=1)

    maxItems = len(item_description.index)
    min_sup = 3
    apriori_without_hashsets(dataset, maxItems, min_sup)

if __name__ == "__main__":
    main()
