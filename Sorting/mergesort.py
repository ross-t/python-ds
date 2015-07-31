# A top-down merge sort
def mergesort(list_to_sort):
	if len(list_to_sort) < 2: # A list of length 1 is sorted by definition
		return list_to_sort

	# Split the list into left and right halves
	midpoint = len(list_to_sort)/2
	right = mergesort(list_to_sort[midpoint:])
	left = mergesort(list_to_sort[:midpoint])

	# Recursively mergesort the left and the right
	right = mergesort(right)
	left = mergesort(left)

	# Then merge them
	return merge(left, right)

def merge(left, right):
	res = list()
	# Add the smallest item from each list onto the result
	while len(left) != 0 and len(right) != 0:
		if left[0] < right[0]:
			res.append(left[0])
			left = left[1:]
		else:
			res.append(right[0])
			right = right[1:]
	# When we're done, either list might have items left
	# If so, we can just add them all to the result as they're guaranteed to be larger
	if len(left) > 0:
		res.extend(left)
	elif len(right) > 0:
		res.extend(right)

	return res

if __name__ == '__main__':
	test_sort = [1, 0, 9, 2, 8, 3, 7, 4, 6, 5]
	print mergesort(test_sort)