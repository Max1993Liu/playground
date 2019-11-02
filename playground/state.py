from abc import ABCMeta, abstractmethod


class State(metaclass=ABCMeta):
	
	@abstractmethod
	def check_result(self, other):
		""" Return the reward given another state """
		pass
