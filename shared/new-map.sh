#!/usr/bin/env bash
# Stamp a new Keystone map folder from the kit. Usage: shared/new-map.sh 05-pharma "Pharmaceuticals"
set -euo pipefail
slug="$1"; name="$2"
root="$(cd "$(dirname "$0")/.." && pwd)"
dest="$root/projects/$slug"
[ -e "$dest" ] && { echo "exists: $dest"; exit 1; }
cp -R "$root/projects/_kit" "$dest"
# substitute the display name into the README
sed -i '' "s/{{NAME}}/$name/g" "$dest/README.md"
# the per-map runbook is a POINTER to the shared _kit procedure, never a copy (a copy rots).
# _kit's full AGENT-RUNBOOK.md was copied in above; replace it so it cannot freeze and drift.
cat > "$dest/AGENT-RUNBOOK.md" <<RUNBOOK
# Agent runbook for projects/$slug

🔴 **Read [\`../_kit/AGENT-RUNBOOK.md\`](../_kit/AGENT-RUNBOOK.md) FIRST. It is the authoritative burst procedure.**

The shared discipline is the single source of truth in \`_kit\` and is deliberately NOT copied here, so it
cannot drift out of a stale copy (this repo's own rule: a copy rots, a pointer does not). That includes:
stage candidate edges in \`data/_incoming/edges_*.csv\`, then run \`tools/verify_edges.py projects/$slug\`,
then merge; file \`data/gaps.csv\` rows as you go; the chokepoint discipline; and closing a burst under one
\`## HONEST WEAKNESSES\` heading with the rows in the same commit.

## Notes for this map
_None yet. Put only routing, sources, or vocabulary for this map here; keep all shared procedure in \`_kit\`._
RUNBOOK
echo "created $dest"
