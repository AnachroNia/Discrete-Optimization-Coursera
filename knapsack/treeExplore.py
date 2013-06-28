import numpy as np
from copy import deepcopy

def get_estimate(mask,values,weights,value,room):
	mask = np.logical_not(mask)
	values = values[mask]
	weights = weights[mask]
	valDensity = values/weights
	valDenIndexes = np.argsort(valDensity)[::-1]
	weights = weights[valDenIndexes]
	values = values[valDenIndexes]
	cumWeights = np.cumsum(weights)
	fittable_value = np.cumsum(values)[cumWeights <= room]
	if len(fittable_value) > 0:
		value += np.cumsum(values)[cumWeights <= room][-1]
	if len(values[cumWeights > room]) > 0:
		partial_value = values[cumWeights > room][0]
		partial_weight = weights[cumWeights > room][0]
		if len(fittable_value) > 0:
			room -= cumWeights[cumWeights <= room][-1]
		value += room/partial_weight*partial_value
	return value

def evaluate(mask,values,weights,capacity):
	room = capacity - np.sum(weights[mask])
	if room < 0:
		value = 0
		estimate = 0
	else:
		value = np.sum(values[mask])
		if np.all(mask):
			estimate = value
		else:
			estimate = get_estimate(mask,values,weights,value,room)
	return value,room,estimate

# values = np.array([45,48,35]).astype(float)
# weights = np.array([5,8,3]).astype(float)
# nItems = len(values)
# capacity = 10

values = np.array([8,10,15,4]).astype(float)
weights = np.array([4,5,8,3]).astype(float)
nItems = len(values)
capacity = 11

# # still_possible = np.array([True,True,True])
# # mask = np.array([False,False,False])
# # print evaluate(mask,values,weights,10)
# cur_item = 0
# configurations = []
# results = [[] for i in xrange(nItems)]
# solutions = []
# still_possible = np.array([True,True,True])
# for i in xrange(5):
# 	if i == 0:
# 		still_possible = np.array([True,True,True])
# 		mask = np.array([False,False,False])
# 		still_possible[0] = False
# 	else:
# 		still_possible,mask = configurations[-1]
# 		still_possible = np.copy(still_possible)
# 		mask = np.copy(mask)
# 		if mask[cur_item]:
# 			still_possible[cur_item] = False
# 		else:
# 			mask[cur_item] = True
# 		# print mask
# 	config_mask = mask[still_possible]
# 	config_values = values[still_possible]
# 	config_weights = weights[still_possible]
# 	# print 'mask',config_mask
# 	# print 'values',config_values
# 	# print 'weights',config_weights
# 	result = evaluate(config_mask,config_values,config_weights,room)
# 	results[cur_item].append(result[-1])
# 	configurations.append((still_possible,mask))
# 	if cur_item == nItems-1:
# 		solutions.append([still_possible,mask,result])
# 	if i == 0:
# 		cur_item += 1
# 	elif still_possible[cur_item] == False:
# 		cur_item += 1
# 	print result

class node(object):
	def __init__(self,parent=None):
		self.parent = parent
		if parent is None:
			self.possible_items = np.array([True for _ in range(nItems)])
			self.current_items = np.array([False for _ in range(nItems)])
			self.current_item = -1
			self.children = 0
		else:
			self.current_items = np.copy(parent.current_items)
			self.current_item = parent.current_item + 1
			self.possible_items = np.copy(parent.possible_items)
			if parent.children == 0:
				self.current_items[self.current_item] = True
			else: 
				self.possible_items[self.current_item] = False
			parent.children += 1
			self.children = 0
		node_mask = self.current_items[self.possible_items]
		node_values = values[self.possible_items]
		node_weights = weights[self.possible_items]
		value,room,estimate = evaluate(node_mask,node_values,node_weights,capacity)
		self.value = value
		self.room = room
		self.estimate = estimate

	def __str__(self):
		return str(self.__dict__)

def answer(solution,solutions):
	print '****SOLUTIONs****'
	for solution in solutions:
		print solution.estimate
	print '****DONE****'

def process(parent):
	if parent.children == 2:
		print 'stepping up tree'
		process(parent.parent)
	else:
		res = node(parent)
	if parent.children == 1:
		if len(solution_values) > 0:
			if res.value < np.max(solution_values):
				print 'done'
				answer(solutions[np.argmax(solution_values)],solutions)
	if res.current_item == nItems-1:
		solution_values.append(res.value)
		solutions.append(res)
	results.append(res)
	print res.value,res.room,res.estimate
	if res.current_item == nItems-1 and res.parent.children == 2:
		process(parent.parent)
	else:
		if res.room < 0 or res.current_item == nItems-1:
			print 'calling on parent'
			process(res.parent)
		else:
			print 'calling on res'
			process(res)

root = node()
results = []
solution_values = []
solutions = []
process(root)
# print root
# print child1
# print child2