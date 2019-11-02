from abc import ABCMeta, abstractmethod


class Strategy(metaclass=ABCMeta):

	@abstractmethod
	def predict(self, env):
		""" Return a tuple of (predicted state, cost),
			Return None if no action is taken at this round
		"""
		pass
