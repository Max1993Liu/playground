from abc import ABCMeta, abstractmethod


class State(metaclass=ABCMeta):
	
	@abstractmethod
	def check_result(self, other):
		""" Return the reward given another state """
		pass


class SSQ(State):

	def __init__(self, date, red, blue):
		self.date = date
		self.red = red
		self.blue = blue

	def check_result(self, other):
		if self.date != other.date:
			raise ValueError('Not from same date')

		if sorted(self.red) == sorted(other.red):
			return 100
		elif self.blue == other.blue:
			return 1
		else:
			return 0
