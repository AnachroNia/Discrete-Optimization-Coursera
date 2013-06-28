import numpy as np

def get_estimate(mask,values,weights,value,room):
	mask = np.logical_not(mask)
	values = values[mask]
	weights = weights[mask]
	valDensity = values/weights
	valDenIndexes = np.argsort(valDensity)[::-1]
	weights = weights[valDenIndexes]
	values = values[valDenIndexes]
	cumWeights = np.cumsum(weights)
	print room
	print cumWeights
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

values = np.array([45,48,35]).astype(float)
weights = np.array([5,8,3]).astype(float)
nItems = len(values)
room = 10

# still_possible = np.array([True,True,True])
# mask = np.array([False,False,False])
# print evaluate(mask,values,weights,10)
cur_item = 0
configurations = []
results = [[] for i in xrange(nItems)]
solutions = []
still_possible = np.array([True,True,True])
for i in xrange(5):
	if i == 0:
		still_possible = np.array([True,True,True])
		mask = np.array([False,False,False])
		still_possible[0] = False
	else:
		still_possible,mask = configurations[-1]
		still_possible = np.copy(still_possible)
		mask = np.copy(mask)
		if mask[cur_item]:
			still_possible[cur_item] = False
		else:
			mask[cur_item] = True
		# print mask
	config_mask = mask[still_possible]
	config_values = values[still_possible]
	config_weights = weights[still_possible]
	# print 'mask',config_mask
	# print 'values',config_values
	# print 'weights',config_weights
	result = evaluate(config_mask,config_values,config_weights,room)
	results[cur_item].append(result[-1])
	configurations.append((still_possible,mask))
	if cur_item == nItems-1:
		solutions.append([still_possible,mask,result])
	if i == 0:
		cur_item += 1
	elif still_possible[cur_item] == False:
		cur_item += 1
	print result