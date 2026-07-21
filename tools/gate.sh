#!/bin/sh
# The gate. Everything this repo claims about itself, checked in one command.
#
#   ./tools/gate.sh
#
# Run it before every commit. Same idea as industrial-index/tools/gate.sh and
# power-service-toolbox/tools/gate.sh: a rule that lives only in a README is a wish.
#
# The risk here is specific. This repo publishes numbers about real companies under a README that
# swears "Sourced or it does not exist". The way that promise dies is not a crash, it is a quiet row
# with a revenue figure and an empty source column, which looks exactly like a sourced row to a reader.
#
# OFFLINE AND FAST ON PURPOSE. No link checking, no network. A gate that needs wifi gives different
# answers on different wifi, a check that flakes gets bypassed, and a bypassed gate is worse than no
# gate: the repo still looks checked.
#
# Incomplete does NOT fail. Incorrect does. Nine of ten maps are foundation briefs with no financials
# by design, and a gate that failed them would be bypassed on day one. See tools/check_data.py.
set -u
cd "$(dirname "$0")/.." || exit 2
fail=0

echo "GATE"
echo ""

echo "[1/4] the checks fire (selftest before any verdict is believed)"
python3 tools/check_data.py --selftest >/dev/null || {
  echo "  SELFTEST FAILED. The checker is broken, so its verdict on the data means nothing."
  echo "  Run: python3 tools/check_data.py --selftest"
  exit 2
}
python3 tools/check_fresh.py --selftest >/dev/null || {
  echo "  SELFTEST FAILED. The freshness checker is broken, so its verdict means nothing."
  echo "  Run: python3 tools/check_fresh.py --selftest"
  exit 2
}
python3 tools/check_identity.py --selftest >/dev/null || {
  echo "  SELFTEST FAILED. The identity checker is broken, so its verdict means nothing."
  echo "  Run: python3 tools/check_identity.py --selftest"
  exit 2
}
python3 tools/xbrl_extract.py --selftest >/dev/null || {
  echo "  SELFTEST FAILED. The extractor's encoded rules (attributable vs consolidated net income,"
  echo "  cash-flow vs additions capex, stale-period rejection) no longer hold."
  echo "  Run: python3 tools/xbrl_extract.py --selftest"
  exit 2
}
echo "  ok, every rule fires on its own mutant"

echo ""
echo "[2/4] data matches what the README promises"
python3 tools/check_data.py || fail=1

echo ""
echo "[3/4] every EDGAR filing cited belongs to the company citing it"
python3 tools/check_identity.py || { fail=1; echo "  a lookup that resolves is not the entity you meant; see shared/edgar_registrants.csv"; }

echo ""
echo "[4/4] every built artifact still renders from its current CSVs"
python3 tools/check_fresh.py || { fail=1; echo "  a committed artifact drifted from its data; rebuild it with shared/build_map.py"; }

echo ""
# The gate answers "is this wrong?". It deliberately does NOT answer "is this over-claimed?", because
# that is a judgement call and a gate that fails on judgement calls gets bypassed. Point at the tool
# that does ask, with its count, so the question stays visible without ever blocking a commit.
adv=$(python3 tools/review.py 2>/dev/null | sed -n 's/.*: \([0-9]*\) must resolve.*/\1/p')
if [ -n "$adv" ] && [ "$adv" != "0" ]; then
  echo "ADVISORY: tools/review.py has $adv finding(s) where a map claims more than it can show."
  echo "  Not a gate failure. Run ./tools/review.py"
  echo ""
fi

if [ "$fail" -ne 0 ]; then
  echo "GATE FAILED. Do not ship."
  exit 1
fi
echo "GATE PASSED."
echo ""
echo "Not checked here, because it needs a browser and a human eye:"
echo "  that the rendered page LOOKS right (layout, colours, no visual overflow)."
echo "  Data drift IS now caught headless by [3/3]; the Browser pane hangs on local file:// anyway."
