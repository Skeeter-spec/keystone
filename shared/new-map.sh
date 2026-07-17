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
echo "created $dest"
