const fs = require("fs");
eval(fs.readFileSync("engine.js", "utf8"));
const exp = JSON.parse(fs.readFileSync("expected.json", "utf8"));
const fns = { gap: gapTruth, floor: floorTruth, middle: middleTruth, ladder: ladderTruth };
let fail = 0;
for (const c of exp.cases) {
  const got = JSON.stringify(fns[c.fn](...c.args));
  if (got !== JSON.stringify(c.expect)) { fail++; console.log("MISMATCH", c.fn, c.args, "\n got:", got, "\n exp:", JSON.stringify(c.expect)); }
}
const ERRS = ["the asking price must be a dollar amount above $0.00, like 45 or 45.00",
  "the offer must be a dollar amount like 30 or 30.00",
  "the floor must be a dollar amount like 32 or 32.00",
  "the rounding step must be one of 0.01, 0.05, 0.10, 0.25, 0.50 or 1.00"];
for (const [fn, args] of exp.errors) {
  let threw = null;
  try { fns[fn](...args); } catch (e) { threw = e.message; }
  if (!threw || !ERRS.includes(threw)) { fail++; console.log("ERRCASE FAIL", fn, args, "->", threw); }
}
console.log(fail ? `${fail} FAILURES` : "all green");
process.exit(fail ? 1 : 0);
