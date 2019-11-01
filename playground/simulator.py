import math

class Simulator:

	def __init__(self,
				selector,
				strategy):
		self.selector = selector
		self.strategy = strategy

		self.reward_history = list()
		self.n_step = 0
		self.decision_history = list()

	def simulate(self, steps=None):
		steps = steps or math.inf

		for s in self.selector:
			self.n_step += 1
			# s is either a single state or a tuple whose last element
			# is the current state
			if isinstance(s, tuple):
				env, cur_state = s[:-1], s[-1]
			else:
				env, cur_state = None, s

			# prepare the environment that would be given to self.strategy
			environ = {}
			environ['state_info'] = env
			environ['reward_history'] = self.reward_history
			environ['step'] = self.n_step

			# evaluate the output
			predicted_state = self.strategy.predict(environ)
			self.decision_history.append(predicted_state)
			self.reward_history.append(cur_state.check_result(predicted_state))

			if self.n_step >= steps:
				break
		