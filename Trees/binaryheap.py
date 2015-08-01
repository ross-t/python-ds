class ExampleBinaryHeap(object):
	def __init__(self):
		self.heap = []

	def insert(self, item):
		'''Insert an item into the heap'''
		self.heap.append(item)
		self.up_heap(len(self.heap) - 1)

	def up_heap(self, item_index):
		'''Bubble the item up the heap until we don't violate the heap property'''
		item_parent = get_parent(self.heap, item_index)
		if item_parent == None:
			return
		if self.heap[item_index] > item_parent:
			parent_index = get_parent_index(item_index)
			swap(self.heap, item_index, parent_index)
			self.up_heap(parent_index)

	def delete_min(self):
		res = self.heap[0]
		self.heap[0] = self.heap[-1]
		self.heap = self.heap[:-1]
		self.down_heap(0)
		return res

	def down_heap(self, item_index):
		children = get_children(self.heap, item_index)
		if children[0] == None and children[1] == None:
			return

		if children[1] == None:
			if self.heap[item_index] > children[0]:
				child_index = get_child_indices(item_index)[0]
				swap(self.heap, item_index, child_index)
				self.down_heap(child_index)
			return

		# The item has two children: swap it with the smaller of the two
		child_indices = get_child_indices(item_index)
		smallest_child = min(children)
		if children[0] == smallest_child and children[0] < self.heap[item_index]:
			# Swap with the left child
			swap(self.heap, item_index, child_indices[0])
			self.down_heap(child_indices[0])
		elif children[1] < self.heap[item_index]:
			# Swap with the right child
			swap(self.heap, item_index, child_indices[1])
			self.down_heap(child_indices[1])

	def find_min(self):
		return self.heap[0]

	def is_empty(self):
		return len(self.heap) == 0

	def size(self):
		return len(self.heap)

	@staticmethod
	def build_heap(list):
		pass

def swap(heap, first_index, second_index):
	temp = heap[first_index]
	heap[first_index] = heap[second_index]
	heap[second_index] = temp

def get_children(heap, parent_index):
	if (2 * parent_index + 1) >= len(heap):
		return (None, None)
	if (2 * parent_index + 2) >= len(heap):
		return (heap[2 * parent_index + 1], None)
	return (heap[2 * parent_index + 1], heap[2 * parent_index + 2])

def get_parent(heap, child_index):
	parent_index = get_parent_index(child_index)
	if parent_index == None:
		return None
	return heap[parent_index]

def get_parent_index(child_index):
	if child_index == 0:
		return None
	return (child_index - 1) // 2

def get_child_indices(parent_index):
	return ((2 * parent_index + 1), (2 * parent_index + 2))

if __name__ == '__main__':
	e = ExampleBinaryHeap()
	e.insert(11)
	e.insert(5)
	e.insert(8)
	e.insert(3)
	e.insert(4)
	e.delete_min()
	print e.heap