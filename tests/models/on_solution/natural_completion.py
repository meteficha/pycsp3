import json

from pycsp3 import *

n = 20
profits = [((i * 13) % 53) + 5 for i in range(n)]
weights = [((i * 5) % 17) + 2 for i in range(n)]

x = VarArray(size=n, dom={0, 1})

satisfy(
    Sum(weights[i] * x[i] for i in range(n)) <= int(sum(weights) * 0.46),
    Sum(x) >= 6,
    Sum(x) <= 11,
)

maximize(
    Sum(profits[i] * x[i] for i in range(n))
)

callback_bounds = []
callback_values = []


def on_solution(inst):
    callback_bounds.append(int(inst.bound))
    callback_values.append([int(v) for v in inst.values])


status = solve(solver='[ace,seed=1]', on_solution=on_solution)
final_values = [int(v) for v in values(x)]
final_objective = sum(profits[i] * final_values[i] for i in range(n))
final_bound = bound()

payload = {
    'status': str(status),
    'callback_count': len(callback_bounds),
    'callback_bounds': callback_bounds,
    'last_callback_values': callback_values[-1] if callback_values else None,
    'final_values': final_values,
    'final_objective': int(final_objective),
    'final_bound': None if final_bound is None else int(final_bound),
}
print('PYCSP3_TEST_RESULT=' + json.dumps(payload))
