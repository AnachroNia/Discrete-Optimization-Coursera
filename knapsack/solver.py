#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

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

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    values = []
    weights = []

    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()

        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    items = len(values)

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = []

    opt_table = build_opt_table(items,capacity,values,weights)
    value = int(opt_table[items,capacity])
    taken = traceback(opt_table,items,capacity,weights)
    # for i in range(0, items):
    #     if weight + weights[i] <= capacity:
    #         taken.append(1)
    #         value += values[i]
    #         weight += weights[i]
    #     else:
    #         taken.append(0)

    # values = np.array(values).astype(float)
    # weights = np.array(weights).astype(float)
    # valDensity = values/weights
    # valDenIndexes = np.argsort(valDensity)[::-1]
    # cumWeights = np.cumsum(weights[valDenIndexes])
    # taken = np.zeros(items)
    # mask = valDenIndexes[cumWeights < capacity]
    # taken[mask] += 1
    # taken = taken.astype(int).tolist()
    # value = int(np.sum(values[mask]))

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(0) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

