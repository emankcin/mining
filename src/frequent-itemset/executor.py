import pandas as pd
from apriori.join import join

raw_dataset = pd.read_csv("../../data/receipts.csv", "r", header=None)[0]

dataset = []
for itemset in raw_dataset:
    tmp = itemset.split(',')
    tmp.pop(0)
    dataset.append(tmp)

#####
dataset = dataset[:60]

item_description = pd.read_csv("../../data/item_description.csv", "r", header=None, delimiter=",", index_col=0, skiprows=1)

maxItems = len(item_description.index)

counts = {}
for i in range(maxItems):
    counts[(i)] = 0

# scan dataset to count single item occurrences
for row in dataset:
    for col in row:
    	key = int(float(col))
        counts[(key)] += 1

for i in range(len(counts)):
    if counts[i] < 5:
        counts.pop((i))

counts = [[i] for i in counts]
result = counts[:]

cont = True
while cont:
	# join list with itself
	k_result = {}
	c = 0
	print "New iteration"
	ci = 0
	resl = list(result)
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
	for i in range(len(k_result)):
		if tuple(k_result[i]) in k_counts and k_counts[tuple(k_result[i])] >= 15:
			counts[tuple(k_result[i])] = k_counts[tuple(k_result[i])]
			cont = True
	result = k_result
	print counts
	if not cont:
		break

print "Frequenet itemsets:"
#for i in counts:
	#print counts