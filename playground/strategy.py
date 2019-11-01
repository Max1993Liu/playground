from abc import ABCMeta, abstractmethod


class Strategy(metaclass=ABCMeta):

	@abstractmethod
	def predict(self, env):
		pass
