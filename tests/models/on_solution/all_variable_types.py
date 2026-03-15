import json

from pycsp3 import *

iv = Var(dom=range(5), id="iv")
sv = Var(dom={"red", "green", "blue"}, id="sv")
ia = VarArray(size=3, dom=range(4), id="ia")
sa = VarArray(size=2, dom={"low", "high"}, id="sa")

satisfy(
    iv >= 2,
    sv != "red",
    Sum(ia) >= 3,
    ia[0] >= ia[1],
    sa[0] != sa[1],
)

maximize(iv + Sum(ia))

callbacks = []


def on_solution(inst):
    callbacks.append({
        "bound": None if inst.bound is None else int(inst.bound),
        "inst_iv": int(inst.value(iv)),
        "inst_sv": str(inst.value(sv)),
        "inst_ia": [int(v) for v in inst.value(ia)],
        "inst_sa": [str(v) for v in inst.value(sa)],
    })


status = solve(solver='[ace,seed=1]', on_solution=on_solution)

payload = {
    "status": str(status),
    "callback_count": len(callbacks),
    "last_callback": callbacks[-1] if callbacks else None,
    "final_iv": int(value(iv)),
    "final_sv": str(value(sv)),
    "final_ia": [int(v) for v in values(ia)],
    "final_sa": [str(v) for v in values(sa)],
    "final_bound": None if bound() is None else int(bound()),
}

print("PYCSP3_TEST_RESULT=" + json.dumps(payload))
