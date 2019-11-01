from abc import ABCMeta, abstractmethod
from operator import attrgetter
import random


class Selector(metaclass=ABCMeta):
	""" A selector takes a bunch of `State`s and 
		pick one at a time based on certain rules
	"""
	@abstractmethod
	def select(self, loc=None):
		pass

	@abstractmethod
	def __iter__(self):
		pass


class RandomSelector(Selector):

	def __init__(self, states, random_state=None):
		self.states = states
		random.shuffle(self.states, random=random_state)

	def select(self, loc=None):
		return self.states.pop()

	def __iter__(self):
		while self.states:
			yield self.select()


class StreamSelector(Selector):
	
	def __init__(self, states, order_field):
		"""
		:param order_field: attribute to order by.
		"""
		self.states = sorted(states, key=attrgetter(order_field))
		self.order_field = order_field

		# build a dictionary from list index to field for faster `select`
		self.field_index = {self.get_field(s):i for i, s in enumerate(self.states)}

	def get_field(self, s):
		return attrgetter(self.order_field)(s)

	def select(self, loc=None):
		index = self.field_index[loc]
		return self.states[:index], self.states[index]

	def __iter__(self):
		for s in self.states:
			yield self.select(self.get_field(s))


class StreamWindowSelector(StreamSelector):
	
	def __init__(self, states, order_field, window_size=5):
		super().__init__(states, order_field)
		self.window_size = window_size

	def select(self, loc=None):
		hist, cur = super().select(loc)
		return hist[-self.window_size:], cur

	def __iter__(self):
		for s in self.states[self.window_size+1:]:
			yield self.select(self.get_field(s))
