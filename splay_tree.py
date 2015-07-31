import unittest

class TreeNode(object):
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = self.right = None

	def __repr__(self):
		if self.left is None and self.right is None:
			return "%s [%s]" % (self.key, self.value)
		elif self.right is None:
			return "%s [%s]: %s," % (self.key, self.value, self.left.key)
		elif self.left is None:
			return "%s [%s]: ,%s" % (self.key, self.value, self.right.key)
		else:
			return "%s [%s]: %s,%s" % (self.key, self.value, self.left.key, self.right.key)

class ExampleSplayTree(object):
	def __init__(self):
		self.root = None
		self.header = TreeNode(None, None)

	def put(self, key, value):
		if self.root == None:
			self.root = TreeNode(key, value)
			return
		self.root = self.splay(self.root, key)
		if key < self.root.key:
			new_node = TreeNode(key, value)
			new_node.left = self.root.left
			new_node.right = self.root
			self.root.left = None
			self.root = new_node
		elif key > self.root.key:
			new_node = TreeNode(key, value)
			new_node.right = self.root.right
			new_node.left = self.root
			self.root.right = None
			self.root = new_node
		else:
			self.root.value = value

	def remove(self, key):
		if self.root == None:
			raise KeyError("Key %s is not in the tree" % key)

		self.root = self.splay(self.root, key)

		if key == self.root.key:
			if self.root.left == None:
				self.root = self.root.right
			else:
				temp = self.root.right
				self.root = self.root.left
				self.splay(self.root, key)
				self.root.right = temp
		else:
			raise KeyError("Key %s is not in the tree" % key)
	
	def get_min(self):
		if self.root is None:
			return None
		current_node = self.root
		while current_node.left != None:
			current_node = current_node.left
		self.splay(current_node.key)
		return current_node

	def get_max(self):
		if self.root is None:
			return None
		current_node = self.root
		while current_node.right != None:
			current_node = current_node.right
		self.splay(current_node.key)
		return current_node

	def get(self, key):
		if self.root is None:
			raise KeyError('Key %s is not in the tree' % key)
		self.root = self.splay(self.root, key)
		if self.root.key != key:
			raise KeyError('Key %s is not in the tree' % key)
		return self.root

	def is_empty(self):
		return self.root == None

	def rotate_right(self, node):
		temp = node.left
		node.left = temp.right
		temp.right = node
		return temp

	def rotate_left(self, node):
		temp = node.right
		node.right = temp.left
		temp.left = node
		return temp

	def splay(self, node, key):
		if node == None:
			return None
		if key < node.key:
			if node.left == None:
				return node
			if key < node.left.key:
				node.left.left = self.splay(node.left.left, key)
				node = self.rotate_right(node)
			elif key > node.left.key:
				node.left.right = self.splay(node.left.right, key)
				if node.left.right != None:
					node.left = self.rotate_left(node.left)
			if node.left == None:
				return node
			else:
				return self.rotate_right(node)
		elif key > node.key:
			if node.right == None:
				return node
			if key < node.right.key:
				node.right.left = self.splay(node.right.left, key)
				if node.right.left != None:
					node.right = self.rotate_right(node.right)
			elif key > node.right.key:
				node.right.right = self.splay(node.right.right, key)
				node = self.rotate_left(node)
			if node.right == None:
				return node
			else:
				return self.rotate_left(node)
		else:
			return node

	def __setitem__(self, key, value):
		self.put(key, value)

	def __getitem__(self, key):
		return self.get(key)

	def __contains__(self, key):
		try:
			return self.get(key)
		except KeyError:
			return False

	def __delitem__(self, key):
		try:
			self.remove(key)
		except KeyError:
			return False


class TestSplayTree(unittest.TestCase):
	def test_put(self):
		t = ExampleSplayTree()
		t.put(5, 5)
		t.put(3, 3)
		t.put(4, 4)
		t.put(7, 7)
		t.put(6, 6)
		self.assertEqual(t.root.key, 6)
		self.assertEqual(t.root.right.key, 7)
		self.assertEqual(t.root.left.key, 5)
		self.assertEqual(t.root.left.left.key, 4)
		self.assertEqual(t.root.left.left.left.key, 3)

	def test_splay(self):
		t = ExampleSplayTree()
		t.put(5, 5)
		t.put(3, 3)
		t.put(4, 4)
		t.put(7, 7)
		t.put(6, 6)

		t.get(4)
		self.assertEqual(t.root.key, 4)
		self.assertEqual(t.root.left.key, 3)
		self.assertEqual(t.root.right.key, 5)

	def test_delete(self):
		t = ExampleSplayTree()
		t.put(5, 5)
		t.put(3, 3)
		t.put(4, 4)
		t.put(7, 7)
		t.put(6, 6)
		t.remove(4)
		t.remove(6)

		self.assertEqual(t.root.key, 5)
		self.assertEqual(t.root.left.key, 3)
		self.assertEqual(t.root.right.key, 7)
		
if __name__ == '__main__':
	unittest.main()