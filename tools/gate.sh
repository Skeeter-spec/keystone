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

echo "[1/2] the checks fire (selftest before any verdict is believed)"
python3 tools/check_data.py --selftest >/dev/null || {
  echo "  SELFTEST FAILED. The checker is broken, so its verdict on the data means nothing."
  echo "  Run: python3 tools/check_data.py --selftest"
  exit 2
}
echo "  ok, every rule fires on its own mutant"

echo ""
echo "[2/2] data matches what the README promises"
python3 tools/check_data.py || fail=1

echo ""
if [ "$fail" -ne 0 ]; then
  echo "GATE FAILED. Do not ship."
  exit 1
fi
echo "GATE PASSED."
echo ""
echo "Not checked here, because it needs a browser and a human eye:"
echo "  the built artifact renders the numbers the CSVs actually hold"
echo "  (rebuild with projects/01-semiconductor/build_artifact.py <date>, then look at it)"
