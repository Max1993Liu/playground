from abc import ABCMeta, abstractmethod


class Strategy(metaclass=ABCMeta):

	@abstractmethod
	def predict(self, environ):
		pass
