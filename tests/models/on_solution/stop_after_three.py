import json
from threading import Event

from pycsp3 import *

n = 36
profits = [((i * 17) % 97) + 3 for i in range(n)]
weights1 = [((i * 7) % 19) + 1 for i in range(n)]
weights2 = [((i * 11) % 23) + 2 for i in range(n)]

x = VarArray(size=n, dom={0, 1})

satisfy(
    Sum(weights1[i] * x[i] for i in range(n)) <= int(sum(weights1) * 0.42),
    Sum(weights2[i] * x[i] for i in range(n)) <= int(sum(weights2) * 0.47),
    Sum(x) >= 10,
    Sum(x) <= 18,
    Sum(x[:18]) >= 5,
    Sum(x[18:]) <= 11,
    Sum((1 if i % 2 == 0 else 2) * x[i] for i in range(n)) >= 22,
)

maximize(
    Sum(profits[i] * x[i] for i in range(n))
)

stop_event = Event()
callback_bounds = []
callback_values = []
stop_requested_at = None


def on_solution(inst):
    global stop_requested_at
    callback_bounds.append(int(inst.bound))
    callback_values.append([int(v) for v in inst.values])
    if stop_requested_at is None and len(callback_bounds) == 3:
        stop_requested_at = 3
        stop_event.set()


status = solve(solver='[ace,seed=1]', on_solution=on_solution, should_stop=stop_event)
final_values = [int(v) for v in values(x)]
final_objective = sum(profits[i] * final_values[i] for i in range(n))
final_bound = bound()

payload = {
    'status': str(status),
    'callback_count': len(callback_bounds),
    'stop_requested_at': stop_requested_at,
    'callback_bounds': callback_bounds,
    'last_callback_values': callback_values[-1] if callback_values else None,
    'final_values': final_values,
    'final_objective': int(final_objective),
    'final_bound': None if final_bound is None else int(final_bound),
}
print('PYCSP3_TEST_RESULT=' + json.dumps(payload))
