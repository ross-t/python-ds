def qsort(list_to_sort):
	smaller = []
	equal = []
	larger = []

	if len(list_to_sort) < 2:
		return list_to_sort
		
	pivot_element = list_to_sort[len(list_to_sort) // 2]
	for item in list_to_sort:
		if item < pivot_element:
			smaller.append(item)
		elif item > pivot_element:
			larger.append(item)
		else:
			equal.append(item)
	return qsort(smaller) + equal + qsort(larger)


if __name__ == '__main__':
	test_sort = [1, 0, 9, 2, 8, 3, 7, 4, 6, 5]
	print qsort(test_sort)