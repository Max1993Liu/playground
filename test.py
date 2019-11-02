from playground.simulator import Simulator
from playground.state import State
from playground.selector import *
from playground.strategy import Strategy



class TestState(State):

	def __init__(self, order):
		self.order = order

	def check_result(self, other):
		return int(self.order==other.order) * 100

	def __repr__(self):
		return '<{}>'.format(self.order)


class DummyStrategy(Strategy):

	def predict(self, environ):
		return environ['state_info'][0][-1], 2


states = [TestState(i) for i in range(1000)]

stream_selector = StreamWindowSelector(states, order_field='order', window_size=5)
strategy = DummyStrategy()

simulator = Simulator(stream_selector, strategy)
simulator.simulate(steps=5)
