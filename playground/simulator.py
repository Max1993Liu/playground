import math


class Simulator:
    def __init__(self, selector, strategy, cost_per_state=2):
        self.selector = selector
        self.strategy = strategy
        self.cost_per_state = cost_per_state

        self.reward_history = list()
        self.cost_history = list()
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
            environ["state_info"] = env  # state_info is a tuple
            environ["reward_history"] = self.reward_history
            environ["step"] = self.n_step
            # temporary fix to add order_field (usually the date) into the environment
            if hasattr(self.selector, 'order_field'):
            	field_name = getattr(self.selector, 'order_field')
            	environ['order_field'] = getattr(cur_state, field_name)

            # evaluate the output
            predicted_state = self.strategy.predict(environ)
            reward = cur_state.check_result(predicted_state)
            self.decision_history.append(predicted_state)
            self.reward_history.append(reward)
            self.cost_history.append(self.cost_per_state)

            print(
                f"Step {self.n_step}: <Reward>: {reward} <Profit>: {sum(self.reward_history) - sum(self.cost_history)} <Decision>: {predicted_state} <Actual>: {cur_state}"
            )

            if self.n_step >= steps:
                break
