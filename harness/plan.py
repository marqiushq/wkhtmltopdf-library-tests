#!/usr/bin/env python3
"""Decides what a run tests: the version of marqius-wkhtmltopdf (given, or the latest),
the machines, and the matrix of library x program x machine. Writes GitHub's step outputs.

    EVENT=schedule python3 harness/plan.py >> "$GITHUB_OUTPUT"

The daily run tests a version only once (when results/<pair>/ is missing), and the
Monday run tests the latest again, so that a change in the world (a site a test loads, a
dependency) shows within a week. A scheduled run tests nothing itself: it starts a run by hand
(dispatch=true) for the pair to test, because a scheduled event does not say whether the repository
is public, and the attestation of the results is signed according to that. Every other event runs."""
import datetime
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNNERS = {"x86-64": "ubuntu-24.04", "arm64": "ubuntu-24.04-arm"}
SETUPS = ("python", "php", "php_extensions", "ruby", "node", "go", "java", "elixir", "otp", "dotnet")
VERSION = re.compile(r"^[0-9]+(\.[0-9]+){1,3}$")


def get(url, token=None):
    req = urllib.request.Request(url, headers={"User-Agent": "wkhtmltopdf-library-tests"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode()
        except OSError as e:
            last = e
    raise SystemExit(f"could not read {url}: {last}")


def version(given, what, read):
    v = (given or "").strip() or read()
    if not VERSION.match(v):
        raise SystemExit(f"{what}: '{v}' is not a version")
    return v


def main():
    env = os.environ
    programs = {p["key"]: p for p in json.loads((ROOT / "programs.json").read_text())["programs"]}
    libraries = json.loads((ROOT / "libraries.json").read_text())["libraries"]

    mq = version(env.get("INPUT_MARQIUS"), "marqius-wkhtmltopdf",
                 lambda: get(programs["marqius"]["latest"]).strip())

    archs = (env.get("INPUT_ARCHS") or env.get("DEFAULT_ARCHS") or "x86-64 arm64").split()
    for a in archs:
        if a not in RUNNERS:
            raise SystemExit(f"unknown machine '{a}': {' or '.join(RUNNERS)}")

    wanted = (env.get("INPUT_LIBRARIES") or "").split()
    known = {lib["key"] for lib in libraries}
    for w in wanted:
        if w not in known:
            raise SystemExit(f"unknown library '{w}': {' '.join(sorted(known))}")
    if wanted:
        libraries = [lib for lib in libraries if lib["key"] in wanted]

    pair = f"marqius-wkhtmltopdf-{mq}"
    run, dispatch = True, False
    if env.get("EVENT") == "schedule":
        filed = all((ROOT / "results" / pair / a / "results.json").exists() for a in archs)
        monday = datetime.datetime.now(datetime.timezone.utc).weekday() == 0
        run, dispatch = False, not filed or monday

    names = {"wkhtmltopdf": programs["wkhtmltopdf"]["name"], "marqius": f"marqius-wkhtmltopdf {mq}"}
    matrix = []
    for lib in libraries:
        for key in ("wkhtmltopdf", "marqius"):
            for a in archs:
                cell = {"library": lib["key"], "program": key, "arch": a, "runner": RUNNERS[a],
                        "title": f"{lib['name']} {lib['release']} · {names[key]}" + (f" · {a}" if len(archs) > 1 else "")}
                cell.update({s: str(lib["setup"].get(s, "")) for s in SETUPS})
                matrix.append(cell)

    out = {"run": "true" if run else "false", "dispatch": "true" if dispatch else "false", "marqius": mq, "pair": pair,
           "archs": json.dumps(archs), "matrix": json.dumps(matrix, separators=(",", ":"))}
    for k, v in out.items():
        print(f"{k}={v}")
    print(f"{pair}: {len(matrix)} cells on {' and '.join(archs)}; run={out['run']} dispatch={out['dispatch']}", file=sys.stderr)


if __name__ == "__main__":
    main()
