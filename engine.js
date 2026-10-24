// Haggle Math engine: haggle arithmetic honesty - the gap between the ask and the offer, where the offer sits against the owner's own floor, the split-the-difference counter rounded to the owner's step, and the halving ladder toward the offer. Exact integer cents, no library, no named constants; every price and the rounding step are the owner's own entries.
function _money(t, err) {
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{1,5})(\.[0-9]{1,2})?$/.exec(t);
  if (!m) throw new Error(err);
  return parseInt(m[1], 10) * 100 + (m[2] ? parseInt((m[2] + "0").slice(1, 3), 10) : 0);
}
function _m(c) { var s = c < 0 ? "-" : ""; c = Math.abs(c); return s + "$" + Math.floor(c / 100) + "." + String(c % 100).padStart(2, "0"); }
function _pl(n, one, many) { return n + (n === 1 ? one : many); }
function _v(n, one, many) { return n === 1 ? one : many; }
var _STEPS = { "0.01": 1, "0.05": 5, "0.10": 10, "0.25": 25, "0.50": 50, "1.00": 100 };
var _A = "the asking price must be a dollar amount above $0.00, like 45 or 45.00";
var _O = "the offer must be a dollar amount like 30 or 30.00";
var _F = "the floor must be a dollar amount like 32 or 32.00";
var _S = "the rounding step must be one of 0.01, 0.05, 0.10, 0.25, 0.50 or 1.00";
function _args(ask, offer, floor, step) {
  var a = _money(ask, _A);
  if (a <= 0) throw new Error(_A);
  var o = _money(offer, _O), f = _money(floor, _F);
  var st = typeof step === "string" ? step.trim() : "";
  var s = _STEPS[st];
  if (!s) throw new Error(_S);
  return [a, o, f, s, st];
}
function _mid(x, o, s) { return Math.floor((x + o + s) / (2 * s)) * s; }
function _pct(o, a) { return (Math.round(o * 1000 / a) / 10).toFixed(1); }
function gapTruth(ask, offer, floor, step) {
  var v = _args(ask, offer, floor, step), a = v[0], o = v[1];
  if (o === a) return "The offer of " + _m(o) + " matches the " + _m(a) + " ask exactly, leaving no gap to split.";
  if (o < a) return "The ask is " + _m(a) + " and the offer is " + _m(o) + ", a gap of " + _m(a - o) + ": the offer is " + _pct(o, a) + "% of the ask.";
  return "The offer is " + _m(o) + " against a " + _m(a) + " ask, " + _m(o - a) + " over the ask at " + _pct(o, a) + "% of it.";
}
function floorTruth(ask, offer, floor, step) {
  var v = _args(ask, offer, floor, step), o = v[1], f = v[2];
  if (o === f) return "Your floor is " + _m(f) + " and the offer of " + _m(o) + " sits right on it.";
  if (o < f) return "Your floor is " + _m(f) + ": the offer of " + _m(o) + " sits " + _m(f - o) + " under it.";
  return "Your floor is " + _m(f) + ": the offer of " + _m(o) + " sits " + _m(o - f) + " over it.";
}
function middleTruth(ask, offer, floor, step) {
  var v = _args(ask, offer, floor, step), a = v[0], o = v[1], s = v[3], st = v[4];
  if (o === a) return "There is no middle to find: the offer already meets the ask.";
  var c = _mid(a, o, s);
  if (c === a || c === o) return "Splitting the difference between " + _m(a) + " and " + _m(o) + " cannot move past " + _m(c) + ": the $" + st + " step is too coarse for a " + _m(Math.abs(a - o)) + " gap.";
  return "Split the difference once, rounded to the nearest $" + st + ": " + _m(c) + ".";
}
function ladderTruth(ask, offer, floor, step) {
  var v = _args(ask, offer, floor, step), a = v[0], o = v[1], s = v[3], st = v[4];
  if (o === a) return "There is no ladder to climb: the offer already meets the ask.";
  var c1 = _mid(a, o, s);
  if (c1 === a || c1 === o) return "The $" + st + " step swallows the " + _m(Math.abs(a - o)) + " gap in one move, to " + _m(c1) + ": there is no halving ladder.";
  var c2 = _mid(c1, o, s), c3 = _mid(c2, o, s);
  return "Keep halving the gap toward the offer: after " + _pl(1, " split", " splits") + " the price lands at " + _m(c1) + ", after " + _pl(2, " split", " splits") + " at " + _m(c2) + ", after " + _pl(3, " split", " splits") + " at " + _m(c3) + ".";
}
