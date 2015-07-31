# A simple hash table implementation for learning purposes. You shouldn't actually use this in real code! Python provides a much better implementation with the default dictionary datatype.

class ExampleHashTable(object):
	def __init__(self, buckets, hash_function=None):
		self.buckets = []
		for x in range(buckets):
			self.buckets.append(list()) # If we did this with self.buckets = [[]] * buckets, we'd end up with a buckets list containing many references to the same list, so we'd really only have one bucket!
		if hash_function is None: # If they didn't pass their own hash function, use Python's default hash()
			self.hash_function = hash
		else:
			self.hash_function = hash_function # Otherwise, use the specified custom one
		self.num_entries = 0

	def insert(self, key, value):
		'''Insert a key/value pair into the hash table.'''
		key_idx = self.get_bucket_index(key)
		# If that value is already associated with that key, we don't need to do anything
		if value in self.buckets[key_idx]:
			return
		# Otherwise, place the value in the bucket that key maps to
		self.buckets[key_idx].append(value)
		self.num_entries += 1

	def remove(self, key, value):
		'''Removes the mapping between a key and a value in the hash table.'''
		index = self.get_bucket_index(key)
		if value in self.buckets[index]:
			self.buckets[index].remove(value)
			self.num_entries -= 1

	def get(self, key):
		'''Retrieve the values in the bucket specified key maps to.'''
		return self.buckets[self.get_bucket_index(key)]

	def get_bucket_index(self, key):
		'''Determine the index the key maps to by hashing it and using the modulus operator to map it onto a bucket.'''
		key_hash = self.hash_function(key)
		return key_hash % len(self.buckets)

	def get_load_factor(self):
		return float(self.num_entries)/len(self.buckets)