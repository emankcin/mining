import pandas as pd

def join(set1, set2):
	if len(set1) != len(set2):
		return []
	else:
		length = len(set1)
		suffixes = [set1.pop(length - 1)]
		suffixes.append(set2.pop(length - 1))
		prefix = set1
		if prefix == set2:
			prefix.extend(suffixes)
			return sorted(prefix)
		else:
			return []

raw_dataset = pd.read_csv("../../data/receipts.csv", "r", header=None)[0]

dataset = []
for itemset in raw_dataset:
    tmp = itemset.split(',')
    tmp.pop(0)
    dataset.append(tmp)

item_description = pd.read_csv("item_description.csv", "r", header=None, delimiter=",", index_col=0, skiprows=1)

maxItems = len(item_description.index)

counts = {}
for i in range(maxItems):
    counts[i] = 0

# scan dataset to count single item occurrences
for row in dataset:
    for col in row:
        counts[int(float(col))] += 1

for i in range(len(counts)):
    if counts[i] < 5000:
        counts.pop(i)

result = counts

temp = counts
temp_2 = []
for t in temp:
	for u in temp:
		temp_2.append(join([t], [u]))

counts_2 = {}
for row in temp_2:
	tup = tuple(row)
	if tup not in counts_2:
		counts_2[tup] = 0
	else:
		counts_2[tup] += 1

counts_22 = counts_2.copy()
for key in counts_22:
	if counts_22[key] < 5000:
		counts_2.pop(key)

if counts_2 == []:
	print("finished")
	for c in counts:
		print(c)
	for c in counts_2:
		print(c)
else:
	print("not finished")
	for c in counts:
		print(c)
	for c in counts_2:
		print(c)