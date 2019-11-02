from collections import Counter

from playground.simulator import Simulator
from playground.state import State
from playground.selector import StreamWindowSelector, StreamSelector
from playground.strategy import Strategy



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


class FrequencyBasedStrategy(Strategy):

	def __init__(self, 
				lookback_period=10,
				by_position=False):
		self.lookback_period = lookback_period
		self.by_position = by_position

	def predict(self, env):
		cur_date = env['order_field']
		prev_states = env['state_info'][0]  # state_info is a tuple
		prev_states = prev_states[-self.lookback_period:]

		