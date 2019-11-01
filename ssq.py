from collections import Counter

from playground.simulator import Simulator
from playground.state import *
from playground.selector import *
from playground.strategy import Strategy



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

		