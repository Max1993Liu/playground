"""
Searchers for best strategy
"""
import itertools
from typing import *
from .simulator import Simulator


def generate_candidates(params: Dict[str, List[Any]]) -> List[Dict]:
	keys = list(params.keys())
	values = [params[k] for k in keys]

	for v in itertools.product(*values):
		yield dict(zip(keys, v))


def grid_search(selector, strategy_cls, strategy_params, steps=None):
	profit = []

	for param in generate_candidates(strategy_params):
		s = Simulator(selector, strategy_cls(**param), verbose=False)
		s.simulate(steps=steps)
		profit.append((s.profit, param))

	profit = sorted(profit, key=lambda x: -x[0])
	return profit[0]
