import math


class Simulator:
    def __init__(self, selector, strategy):
        self.selector = selector
        self.strategy = strategy
        
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
            decision = self.strategy.predict(environ)
            if decision is None:
                # no action is taken at this step
                predicted_state, reward, cost = None, 0, 0
            else:
                predicted_state, cost = decision
                reward = cur_state.check_result(predicted_state)

            self.decision_history.append(predicted_state)
            self.reward_history.append(reward)
            self.cost_history.append(cost)

            print(
                f"Step {self.n_step}: <Round Reward>: {reward} <Total Reward>: {sum(self.reward_history)} <Profit>: {sum(self.reward_history) - sum(self.cost_history)}" 
            )

            print(
                f"Step {self.n_step}: <Decision>: {predicted_state} <Actual>: {cur_state}"
            )

            print('=' * 128)

            if self.n_step >= steps:
                break
