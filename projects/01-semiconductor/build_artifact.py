#!/usr/bin/env python3
"""Kept so the documented command still works. The renderer now lives in shared/build_map.py.

    python3 build_artifact.py 2026-07-16

This is a SHIM, not a copy. The template that used to sit in artifact/template.html was deleted on
2026-07-16 rather than left behind: a superseded copy is a footgun, because editing it changes
nothing and gives no error. Per-map config is map.json; the shared renderer + template serve all ten
maps. See shared/build_map.py.
"""
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).parent
date = sys.argv[1] if len(sys.argv) > 1 else "unbuilt"
sys.exit(subprocess.call([sys.executable, str(ROOT.parent.parent / "shared" / "build_map.py"),
                          str(ROOT), date]))
