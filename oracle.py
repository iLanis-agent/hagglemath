#!/usr/bin/env python3
# Haggle Math oracle - independent mirror of engine.js; writes expected.json.
import json

STEPS = {"0.01": 1, "0.05": 5, "0.10": 10, "0.25": 25, "0.50": 50, "1.00": 100}

def money(t):
    t = t.strip()
    parts = t.split(".")
    assert parts[0].isdigit() and 1 <= len(parts[0]) <= 5
    if len(parts) == 1: return int(parts[0]) * 100
    assert len(parts) == 2 and parts[1].isdigit() and 1 <= len(parts[1]) <= 2
    return int(parts[0]) * 100 + int((parts[1] + "0")[:2])

def fm(c):
    s = "-" if c < 0 else ""
    c = abs(c)
    return f"{s}${c // 100}.{str(c % 100).zfill(2)}"

def pl(n, one, many): return f"{n}{one if n == 1 else many}"

def args(ask, offer, floor, step):
    a = money(ask); assert a > 0
    o = money(offer); f = money(floor)
    st = step.strip(); s = STEPS[st]
    return a, o, f, s, st

def mid(x, o, s): return ((x + o + s) // (2 * s)) * s
def pct(o, a): return f"{round(o * 1000 / a) / 10:.1f}"

def gap_t(ask, offer, floor, step):
    a, o, f, s, st = args(ask, offer, floor, step)
    if o == a: return f"The offer of {fm(o)} matches the {fm(a)} ask exactly, leaving no gap to split."
    if o < a: return f"The ask is {fm(a)} and the offer is {fm(o)}, a gap of {fm(a - o)}: the offer is {pct(o, a)}% of the ask."
    return f"The offer is {fm(o)} against a {fm(a)} ask, {fm(o - a)} over the ask at {pct(o, a)}% of it."

def floor_t(ask, offer, floor, step):
    a, o, f, s, st = args(ask, offer, floor, step)
    if o == f: return f"Your floor is {fm(f)} and the offer of {fm(o)} sits right on it."
    if o < f: return f"Your floor is {fm(f)}: the offer of {fm(o)} sits {fm(f - o)} under it."
    return f"Your floor is {fm(f)}: the offer of {fm(o)} sits {fm(o - f)} over it."

def middle_t(ask, offer, floor, step):
    a, o, f, s, st = args(ask, offer, floor, step)
    if o == a: return "There is no middle to find: the offer already meets the ask."
    c = mid(a, o, s)
    if c == a or c == o: return f"Splitting the difference between {fm(a)} and {fm(o)} cannot move past {fm(c)}: the ${st} step is too coarse for a {fm(abs(a - o))} gap."
    return f"Split the difference once, rounded to the nearest ${st}: {fm(c)}."

def ladder_t(ask, offer, floor, step):
    a, o, f, s, st = args(ask, offer, floor, step)
    if o == a: return "There is no ladder to climb: the offer already meets the ask."
    c1 = mid(a, o, s)
    if c1 == a or c1 == o: return f"The ${st} step swallows the {fm(abs(a - o))} gap in one move, to {fm(c1)}: there is no halving ladder."
    c2 = mid(c1, o, s); c3 = mid(c2, o, s)
    return f"Keep halving the gap toward the offer: after {pl(1, ' split', ' splits')} the price lands at {fm(c1)}, after {pl(2, ' split', ' splits')} at {fm(c2)}, after {pl(3, ' split', ' splits')} at {fm(c3)}."

cases, errors = [], []
def C(fn, *a): cases.append({"fn": fn, "args": [str(x) for x in a], "expect": globals()[fn + "_t"](*[str(x) for x in a])})

D = ("45.00", "30.00", "32.00", "0.25")
for fn in ["gap", "floor", "middle", "ladder"]: C(fn, *D)
asks = ["1.00", "9.99", "25", "100.00", "250.50", "999.99", "45.00", "12.50", "99999.99", "3.30"]
offers = ["0.01", "7.50", "25", "80.00", "200.25", "1.00", "50.00", "12.50", "50000.00", "3.30"]
floors = ["0.00", "7.50", "20.00", "80.00", "220.00", "0.99", "32.00", "10.00", "60000.00", "3.00"]
steps = ["0.01", "0.05", "0.10", "0.25", "0.50", "1.00", "0.25", "0.05", "1.00", "0.01"]
for a, o, f, s in zip(asks, offers, floors, steps):
    for fn in ["gap", "floor", "middle", "ladder"]: C(fn, a, o, f, s)
# offer over ask, on the floor, tiny gaps and coarse-step stalls
extra = [("45.00", "50.00", "32.00", "0.25"), ("45.00", "45.00", "45.00", "0.25"),
         ("10.00", "9.90", "9.50", "0.25"), ("10.00", "9.70", "9.50", "0.25"),
         ("0.01", "0.00", "0.00", "0.01"), ("60.00", "40.00", "50.00", "1.00"),
         ("60.00", "50.00", "50.00", "0.50"), ("19.99", "15.01", "16.00", "0.05"),
         ("200.00", "150.00", "150.00", "0.10"), ("8.00", "2.00", "3.00", "1.00"),
         ("45.00", "44.75", "40.00", "0.25"), ("45.00", "0.00", "0.00", "0.01")]
for a, o, f, s in extra:
    for fn in ["gap", "floor", "middle", "ladder"]: C(fn, a, o, f, s)

bad = [("gap", ["0", "30.00", "32.00", "0.25"]), ("gap", ["abc", "30.00", "32.00", "0.25"]),
       ("gap", ["45.001", "30.00", "32.00", "0.25"]), ("gap", ["100000", "30.00", "32.00", "0.25"]),
       ("floor", ["45.00", "-5", "32.00", "0.25"]), ("floor", ["45.00", "30.0.0", "32.00", "0.25"]),
       ("floor", ["45.00", "", "32.00", "0.25"]), ("floor", ["45.00", "30.00", "x", "0.25"]),
       ("middle", ["45.00", "30.00", "32.005", "0.25"]), ("middle", ["45.00", "30.00", "32.00", "0.30"]),
       ("middle", ["45.00", "30.00", "32.00", ""]), ("middle", ["45.00", "30.00", "32.00", "1"]),
       ("ladder", ["45,00", "30.00", "32.00", "0.25"]), ("ladder", ["45.00", "30.00", "32.00", ".25"]),
       ("gap", ["45.00", "30.00", "32.00", "0.25x"]), ("floor", ["  ", "30.00", "32.00", "0.25"])]
for fn, a in bad: errors.append([fn, a])

json.dump({"cases": cases, "errors": errors}, open("expected.json", "w"), indent=1)
print(len(cases), "cases,", len(errors), "errcases")
