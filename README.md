# Haggle Math

Haggle arithmetic honesty: the gap, the floor position, the split-the-difference counter and the halving ladder.

Live: https://ilanis-agent.github.io/hagglemath/ (landing at `index.html`, app at `app.html`)

## What it does

Four truths from exact integer-cent arithmetic over your own numbers:

1. **Gap** - the distance between the ask and the offer, in dollars and as a share of the ask.
2. **Floor** - where the offer sits against your own walk-away floor: over it, under it or right on it, by exact dollars.
3. **Middle** - one split of the difference, rounded to your step, with an honest stall message when the step is too coarse for the gap.
4. **Ladder** - where the price lands after 1 split, 2 splits and 3 splits of the remaining gap, so convergence is visible before you say a number out loud.

## Files

- `app.html` / `index.html` - the pages
- `engine.js` - the arithmetic (integer cents, no library)
- `oracle.py` - independent mirror that writes `expected.json`
- `test.js` - runs every case in `expected.json` against `engine.js`

## Test

```
python3 oracle.py   # regenerate expected.json
node test.js        # all green
```

## Boundary

Arithmetic only. No named constants: every price and the rounding step are the owner's own entries. The page does not know what the item is worth and gives no verdict that you should take or refuse a deal.
