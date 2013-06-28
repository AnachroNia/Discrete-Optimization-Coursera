import numpy as np

v = [5,6,3]
w = [4,5,2]
k = 9
j = 3

def build_opt_table(j,k,v,w):
	opt_table = np.zeros((j+1,k+1))
	for j in xrange(j+1):
		for k in xrange(k+1):
			if j == 0:
				opt_table[j,k] = 0
			elif w[j-1] <= k:
				opt_table[j,k] = max(opt_table[j-1,k],v[j-1]+opt_table[j-1,k-w[j-1]])
			else:
				opt_table[j,k] = opt_table[j-1,k]
	return opt_table

def traceback(opt_table,j,k,w):
	taken = []
	for j in reversed(xrange(j+1)):
		print j
		if opt_table[j,k] == opt_table[j-1,k]:
			taken.append(0)
		else:
			taken.append(1)
			k -= w[j-1]
	taken = taken[::-1]
	del taken[0]
	return taken

# inputDataFile = open('data/ks_10000_0', 'r')
# inputData = ''.join(inputDataFile.readlines())
# inputDataFile.close()

# lines = inputData.split('\n')

# firstLine = lines[0].split()
# items = int(firstLine[0])
# capacity = int(firstLine[1])

# values = []
# weights = []

# for i in range(1, items+1):
#     line = lines[i]
#     parts = line.split()

#     values.append(int(parts[0]))
#     weights.append(int(parts[1]))

# items = len(values)

# opt_table = np.zeros((items+1,capacity+1))
# print opt_table.size
opt_table = build_opt_table(j,k,v,w)
taken = traceback(opt_table,j,k,w)
value = opt_table[j,k]
print taken
print opt_table
print value