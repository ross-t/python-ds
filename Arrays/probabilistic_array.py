import random

class ProbabilisticArray(object):
	def __init__(self):
		self.map = {}
		self.normalized = False # Track whether the map is currently normalized; if not, then 

	def __setitem__(self, key, value):
		self.normalized = False
		'''Set the probability of key to a given value. If the value is zero, the key will be removed from the ProbabilisticArray'''
		if value < 0:
			raise ValueError("Probability cannot be negative")
		elif value == 0:
			del(self[key])
		else:
			self.map[key] = float(value)

	def __getitem__(self, key):
		'''Returns the probability of accessing a given item in the ProbabilisticArray. If the key does not exist in the array, the probability is zero.'''
		if key in self.map:
			return self.map[key]
		return 0.0

	def _sum(self):
		'''Returns the sum of the probabilities of the items in the array.'''
		return sum(self.map.values())

	def pick(self):
		'''Randomly picks an item out of the array, weighted by probability.'''
		if not self.normalized:
			ProbabilisticArray.normalize(self)

		# Thanks, Rohit J @ https://stackoverflow.com/questions/4463561/weighted-random-selection-from-array
		n = random.uniform(0, 1)
		for key, probability in self.map.items():
			if n < probability:
				break
			n -= probability
		return key

	def __add__(self, other):
		if not isinstance(other, ProbabilisticArray):
			raise TypeError('Cannot add ProbabilisticArray and %s' % str(type(other)))
		else:
			new = ProbabilisticArray()
			for key, probability in self.map.items():
				new[key] = probability
			for key, probability in other.map.items():
				if key in new.map:
					new[key] += probability
				else:
					new[key] = probability
			ProbabilisticArray.normalize(new)
			return new

	def __sub__(self, other):
		if not isinstance(other, ProbabilisticArray):
			raise TypeError('Cannot subtract ProbabilisticArray and %s' % str(type(other)))
		else:
			new = ProbabilisticArray()
			for key, probability in self.map.items():
				new[key] = probability
			for key, probability in other.map.items():
				if key in new.map:
					new_probability = new[key] - probability
					if new_probability <= 0.0:
						del new[key]
					else:
						new[key] = new_probability
			ProbabilisticArray.normalize(new)
			return new

	def __delitem__(self, item):
		del self.map[item]

	@staticmethod
	def normalize(array_to_normalize):
		'''Normalize the probabilities in an array so that the sum of the entries is 1.'''
		if not array_to_normalize.normalized:
			array_sum = array_to_normalize._sum()
			for key in array_to_normalize.map.keys():
				value = array_to_normalize.map[key]
				array_to_normalize.map[key] = value / array_sum
			array_to_normalize.normalized = True