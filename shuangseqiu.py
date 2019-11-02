from collections import Counter
import random
import pickle as pkl
import datetime

from playground.simulator import Simulator
from playground.state import State
from playground.selector import StreamWindowSelector, StreamSelector
from playground.strategy import Strategy



class SSQ(State):

	def __init__(self,
				date, 
				red_balls,
				blue_ball,
				sales=None,
				pool_size=None,
				price_count=None,
				price_money=None
				):
		self.date = date
		self.red_balls = red_balls
		self.blue_ball = blue_ball
		self.pool_size = pool_size
		self.sales = sales
		self.price_count = price_count
		self.price_money = price_money

	@classmethod
	def from_prediction(cls, date, red_balls, blue_ball):
		return cls(date=date, red_balls=red_balls, blue_ball=blue_ball)

	@classmethod
	def random(cls, date, seed=None):
		random.seed(seed)
		red_balls = random.sample(range(1, 34), k=6)
		blue_ball = random.choice(range(1,  17))
		return cls.from_prediction(date, red_balls, blue_ball)

	def check_result(self, other):
		if self.date != other.date:
			raise ValueError('Not from same date')

		n_match_red = self.number_of_matches(self.red_balls, other.red_balls)
		is_match_blue = (self.blue_ball == other.blue_ball)

		if n_match_red == 6 and is_match_blue:
			# 一等奖
			return self.price_money[1]
		elif n_match_red == 6 and not is_match_blue:
			# 二等奖
			return self.price_money[2]
		elif n_match_red == 5 and is_match_blue:
			# 三等奖
			return self.price_money[3]
		elif (n_match_red == 5 and not is_match_blue) or (n_match_red == 4 and is_match_blue):
			# 四等奖
			return self.price_money[4]
		elif (n_match_red == 4 and not is_match_blue) or (n_match_red == 3 and is_match_blue):
			# 五等奖
			return self.price_money[5]
		elif n_match_red in (0, 1, 2) and is_match_blue:
			# 六等奖
			return self.price_money[6]
		else:
			return 0

	def number_of_matches(self, a, b):
		return len(set(a) & set(b))

	def __repr__(self):
		return '<date: {} red: {} blue: {}>'.format(self.date, self.red_balls, self.blue_ball)


def load_history(data_path=None, start_date=None, end_date=None):
	""" Get the actual ticket result between start date and end date (inclusive), 
		start_date and end_date can be datetime object of string of format 'yyyy-mm-dd'

		ex. load_history(start_date='2019-09-01', end_date='2019-10-01')  # 12 records
	"""
	start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date() if isinstance(start_date, str) else start_date
	end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date() if isinstance(end_date, str) else end_date

	data_path = data_path or './data/shuangseqiu.pkl'
	with open(data_path, 'rb') as f:
		history = pkl.load(f)

	history_states = [SSQ(**i) for i in history \
						if (start_date is None or start_date <= i['date']) and (end_date is None or end_date >= i['date'])]
	return history_states



#########################################
# Implementing some basic strategy ######
#########################################

COST_PER_TICKET = 2

class RandomSelectingStrategy(Strategy):

	def predict(self, env):
		cur_date = env['order_field']
		return SSQ.random(cur_date), COST_PER_TICKET


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

		



if __name__ == '__main__':
	states = load_history(start_date='2019-01-01')
	stream_selector = StreamSelector(states, order_field='date')
	strategy = RandomSelectingStrategy()

	simulator = Simulator(stream_selector, strategy)
	simulator.simulate()

