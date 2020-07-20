import math


class Simulator:
    def __init__(self, selector, strategy, verbose=True):
        self.selector = selector
        self.strategy = strategy
        self.verbose = verbose
        
        self.reward_history = list()
        self.cost_history = list()
        self.n_step = 0
        self.decision_history = list()

    @property
    def reward(self):
        return sum(self.reward_history)
    
    @property
    def cost(self):
        return sum(self.cost_history)

    @property
    def profit(self):
        return self.reward - self.cost

    def reset(self):
        self.reward_history = list()
        self.cost_history = list()
        self.n_step = 0
        self.decision_history = list()

    def simulate(self, steps=None):
        self.reset()
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
                # a better error message
                if not isinstance(decision, (tuple, list)):
                    raise ValueError('The strategy should return a tuple of (action, cost).')
                predicted_state, cost = decision
                reward = cur_state.check_result(predicted_state)

            self.decision_history.append(predicted_state)
            self.reward_history.append(reward)
            self.cost_history.append(cost)

            if self.verbose:
                print(
                    f"Step {self.n_step}: <Round Reward>: {reward} <Total Reward>: {self.reward} <Profit>: {self.profit}" 
                )

                print(
                    f"Step {self.n_step}: <Decision>: {predicted_state} <Actual>: {cur_state}"
                )

                print('=' * 128)

            if self.n_step >= steps:
                break

        if self.verbose:
            print(f"Total steps: {self.n_step} <Profit>: {self.profit} <Profit per step>: {self.profit / self.n_step} <Max Reward>: {max(self.reward_history)}")