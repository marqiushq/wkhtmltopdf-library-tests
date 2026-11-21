#!/usr/bin/env python3
"""Files one run's cells under results/PAIR/ARCH/ and writes the README's table from the newest
pair of versions on file. Nothing in it is written by hand: the versions, the counts and every
failure's reason come from the run.

    python3 harness/publish.py ARTIFACTS PROGRAMS_JSON [--message FILE]
    python3 harness/publish.py ARTIFACTS PROGRAMS_JSON --summary FILE --dry-run

A replacement keeps up with a library when every test that passes with wkhtmltopdf 0.12.6 passes
with it too; a test that fails with wkhtmltopdf 0.12.6 as well is shown, not held against it."""
import argparse
import datetime
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRAMS = ("wkhtmltopdf", "marqius", "pdfkiln")
START, END = "<!-- results:start -->", "<!-- results:end -->"


def load_notes():
    """notes.tsv: library, programs (* or names), test (a regular expression), reason (one), note.
    A note explains a failure in plain words, and shows only while a failure matches it."""
    rows = []
    p = ROOT / "notes.tsv"
    for line in (p.read_text().splitlines() if p.exists() else []):
        if not line.strip() or line.startswith("#"):
            continue
        lib, progs, test, reason, note, counted = line.split("\t")
        rows.append((lib, progs, re.compile(test), re.compile(reason), note, counted.strip() != "no"))
    return rows


NOTES = load_notes()


def note_for(lib, prog, test, reason):
    for l, progs, t, r, note, _ in NOTES:
        if l == lib and (progs == "*" or prog in progs.split(",")) and t.search(test) and r.search(reason or ""):
            return note
    return None


def excused(lib, prog, test, reason):
    """True for a failure that a note marked counted: no explains: a test that drives another program
    instead of wkhtmltopdf, or one in which the program never ran. The first note that matches decides,
    as it decides which note is shown, so a failure is excused only while its note matches it."""
    for l, progs, t, r, _, c in NOTES:
        if l == lib and (progs == "*" or prog in progs.split(",")) and t.search(test) and r.search(reason or ""):
            return not c
    return False


def reason_of(cell, test):
    """What the runner said about TEST in CELL ("missing" when the cell has no such test)."""
    v = cell["tests"].get(test)
    return "missing" if v is None else (v[1] if len(v) > 1 else "")


def plain(reason):
    """A runner's reason without the parts that change from run to run (temporary names, numbers)."""
    reason = re.sub(r"/tmp/\S+", "/tmp/…", reason or "")
    return re.sub(r"\b[0-9a-f]{8,}\b|\d{3,}", "#", reason)


def why_lines(lib_list, by, versions):
    """What fails, and why: one line for each kind of failure. Tests are grouped by their reason and
    by the programs they fail with, so that each line counts exactly what it says."""
    n = names(versions)
    groups = {}
    for lib in lib_list:
        per_test = {}
        for p in PROGRAMS:
            c = by.get(lib["key"], {}).get(p)
            if not c or c["state"] == "did not run":
                continue
            for t, v in c["tests"].items():
                if v[0] == "fail":
                    note = note_for(lib["key"], p, t, v[1])
                    per_test.setdefault((t, note or plain(v[1]) or "no reason given"),
                                        {"programs": set(), "note": note, "said": v[1], "excused": excused(lib["key"], p, t, v[1])})["programs"].add(p)
        for (t, why), d in per_test.items():
            if d["excused"]:
                d["programs"] = set(PROGRAMS)  # shown once, whichever programs it failed with this time
            key = (lib["key"], why, frozenset(d["programs"]))
            g = groups.setdefault(key, {"lib": lib, "tests": set(), "programs": d["programs"], "note": d["note"], "said": d["said"], "excused": d["excused"]})
            g["tests"].add(t)
    order = {lib["key"]: i for i, lib in enumerate(lib_list)}
    rank = lambda g: (len(g["programs"]) != 3, "wkhtmltopdf" not in g["programs"], order[g["lib"]["key"]])
    out = []
    for g in sorted(groups.values(), key=rank):
        k = len(g["tests"])
        if g["excused"]:
            who = "not counted"
        else:
            who = "with all three programs" if len(g["programs"]) == 3 else "with " + " and ".join(n[p] for p in PROGRAMS if p in g["programs"])
        why = g["note"] or (f"The test runner says: “{g['said']}”" if g["said"] else "The test runner gives no reason.")
        out.append(f"- **{g['lib']['name']}**, {k} {'test' if k == 1 else 'tests'}, {who}. {why}")
    return out


def vkey(v):
    return tuple(int(x) for x in re.findall(r"\d+", v))


def load_cells(artifacts):
    cells = []
    for p in sorted(Path(artifacts).glob("*/cell.json")):
        cells.append(json.loads(p.read_text()))
    return cells


def names(versions):
    return {"wkhtmltopdf": "wkhtmltopdf 0.12.6", "marqius": f"marqius-wkhtmltopdf {versions['marqius']}",
            "pdfkiln": f"PDFKiln {versions['pdfkiln']}"}


def judge(base, cell):
    """How CELL compares with the baseline: (word, tests lost, tests gained). Lost: pass with
    wkhtmltopdf 0.12.6, not here. Gained: fail with wkhtmltopdf 0.12.6, pass here. A failure that a
    note marked counted: no explains is left out of both."""
    if cell is None or cell["state"] == "did not run":
        return "did not run", [], []
    if base is None or base["state"] == "did not run":
        return ("passed" if cell["state"] == "passed" else "failed"), [], []
    lib = cell["library"]
    prog = cell["program"]
    lost = sorted(t for t, v in base["tests"].items() if v[0] == "pass" and cell["tests"].get(t, ["missing"])[0] != "pass"
                  and not excused(lib, prog, t, reason_of(cell, t)))
    gained = sorted(t for t, v in base["tests"].items() if v[0] == "fail" and cell["tests"].get(t, ["missing"])[0] == "pass"
                    and not excused(lib, "wkhtmltopdf", t, reason_of(base, t)))
    if cell["state"] == "no results":
        return "no results", lost, gained
    return ("keeps up" if not lost else "behind"), lost, gained


def counts_text(cell):
    if cell is None or cell["state"] == "did not run":
        return "did not run"
    c = cell["counts"]
    if not c["tests"]:
        return "no tests reported"
    parts = [f"{c['passed']} passed"]
    if c["failed"]:
        parts.append(f"{c['failed']} failed")
    if c["skipped"]:
        parts.append(f"{c['skipped']} skipped")
    return ", ".join(parts)


def keeps_up(lib_list, by):
    """For each replacement: in how many libraries every counted test that passes with wkhtmltopdf 0.12.6 passes."""
    return {p: sum(judge(by.get(x["key"], {}).get("wkhtmltopdf"), by.get(x["key"], {}).get(p))[0] == "keeps up" for x in lib_list)
            for p in ("marqius", "pdfkiln")}


def table(lib_list, by, versions, run_url, arch, date, other=None):
    """The README's block: a headline per replacement, the table, what the marks mean; OTHER, the
    same pair's results on the other kind of machine, adds a line."""
    n = names(versions)
    rows, keeps = [], {"marqius": 0, "pdfkiln": 0}
    missing = {"marqius": [], "pdfkiln": []}
    never, unbased = [], []
    for lib in lib_list:
        cells = by.get(lib["key"], {})
        base = cells.get("wkhtmltopdf")
        ran = [c for c in cells.values() if c and c["state"] != "did not run"]
        tests = max((c["counts"]["tests"] for c in ran), default=0)
        calls = base["calls"] if base and base["state"] != "did not run" else (ran[0]["calls"] if ran else None)
        if ran and all(c["calls"] == 0 for c in ran):
            never.append(lib["name"])
        if not base or base["state"] == "did not run":
            unbased.append(lib["name"])
        row = [f"[{lib['name']}](https://github.com/{lib['repo']}/tree/{lib['commit']}) {lib['release'].lstrip('vV')}",
               lib["language"], str(tests) if tests else "–", str(calls) if calls is not None else "–", counts_text(base)]
        for p in ("marqius", "pdfkiln"):
            word, lost, _ = judge(base, cells.get(p))
            if word == "keeps up":
                keeps[p] += 1
                row.append(f"✓ {counts_text(cells.get(p))}")
            elif word == "behind":
                row.append(f"✗ {counts_text(cells.get(p))} ({len(lost)} {'test that passes' if len(lost) == 1 else 'tests that pass'} with wkhtmltopdf)")
            else:
                if lib["name"] not in unbased:
                    missing[p].append(lib["name"])
                row.append(counts_text(cells.get(p)))
        rows.append(row)
    total = len(lib_list)
    def unrun(p):
        m = missing[p]
        return f" ({', '.join(m)} did not run)" if m else ""

    head = (f"With **{n['marqius']}**, every test that passes with wkhtmltopdf 0.12.6 also passes in **{keeps['marqius']} of {total}** "
            f"libraries{unrun('marqius')}. With **{n['pdfkiln']}**, in **{keeps['pdfkiln']} of {total}**{unrun('pdfkiln')}.")
    if unbased:
        head += (f" {', '.join(unbased)} could not be compared in this run: wkhtmltopdf 0.12.6's "
                 f"{'run' if len(unbased) == 1 else 'runs'} did not finish (see the run).")
    line = (f"Run of {date} on GitHub's Ubuntu 24.04 machines ({arch}): [the run and its logs]({run_url}), "
            f"[every failure and its reason](results/{versions['pair']}/{arch}/report.md).")
    if other:
        ob = {}
        for c in other["cells"]:
            ob.setdefault(c["library"], {})[c["program"]] = c
        k = keeps_up(other["libraries"], ob)
        shown = {"arm64": "ARM64", "x86-64": "x86-64"}[other["arch"]]
        line += (f" On {shown} machines ([run of {other['date']}]({other['run_url']}), [report](results/{versions['pair']}/{other['arch']}/report.md)): "
                 f"{n['marqius']} in {k['marqius']} of {len(other['libraries'])}, {n['pdfkiln']} in {k['pdfkiln']} of {len(other['libraries'])}.")
    out = [START, "", head, "", line, "",
           f"| Library | Language | Tests | Program runs | wkhtmltopdf 0.12.6 | {n['marqius']} | {n['pdfkiln']} |",
           "|---|---|--:|--:|---|---|---|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    out += ["",
            "✓ every test that passes with wkhtmltopdf 0.12.6 passes with this program too. "
            "✗ some do not: the number in brackets. The figures are what each test runner reported; a test that fails with wkhtmltopdf 0.12.6 too, "
            "or that drives another program instead of wkhtmltopdf (marked “not counted” below), is not held against either program. "
            "Program runs: how many times the suite started wkhtmltopdf or wkhtmltoimage."]
    if never:
        out += ["", f"{', '.join(never)}: {'its' if len(never) == 1 else 'their'} tests never start the program. "
                "They check the library's own code (the command it builds, its settings), so they pass whatever program is installed, or none."]
    why = why_lines(lib_list, by, versions)
    if why:
        out += ["", "**What fails, and why.** Failures that wkhtmltopdf 0.12.6 has too come first: they are not held against either program.", ""] + why
    out += ["", END]
    return "\n".join(out)


def report(lib_list, by, versions, programs, run_url, arch, date):
    """results/PAIR/ARCH/report.md: everything the run found, library by library."""
    n = names(versions)
    files = {(f["program"], f["arch"]): f for f in programs.get("files", [])}
    out = [f"# Library test suites: {n['marqius']} and {n['pdfkiln']}, with wkhtmltopdf 0.12.6", "",
           f"Run of {date} on GitHub's Ubuntu 24.04 machines ({arch}): {run_url}", "",
           "## The programs", "", "| Program | File | SHA-256 | Checked against | Provenance attestation | Says (`wkhtmltopdf -V`) |", "|---|---|---|---|---|---|"]
    says = {}
    for lib in lib_list:
        for p in PROGRAMS:
            c = by.get(lib["key"], {}).get(p)
            if c and c.get("installed") and p not in says:
                says[p] = c["installed"].get("says_pdf", "")
    for p in PROGRAMS:
        f = files.get((p, arch), {})
        out.append(f"| {n[p]} | [{f.get('file', '')}]({f.get('url', '')}) | `{f.get('sha256', '')[:16]}…` | {f.get('checked', '')} | {f.get('attestation', 'not checked')} | `{says.get(p, '')}` |")
    out += ["", "## The libraries", ""]
    for lib in lib_list:
        cells = by.get(lib["key"], {})
        base = cells.get("wkhtmltopdf")
        ran_on = next((c.get("ran_on", {}) for c in (cells.get(p) for p in PROGRAMS) if c and c.get("ran_on")), {})
        out += [f"### {lib['name']} {lib['release']} ({lib['language']})", "",
                f"[{lib['repo']} at {lib['commit'][:7]}](https://github.com/{lib['repo']}/tree/{lib['commit']}), run as its CI runs it: `{lib['runs']}`."
                + (f" {ran_on['runtime']}, on {ran_on.get('system', 'Ubuntu')}"
                   + (f" ({ran_on['image']})" if ran_on.get("image") else "") + "." if ran_on.get("runtime") else "")
                + (f" Runtime: {lib['runtime_note']}." if lib.get("runtime_note") else ""), "",
                "| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |", "|---|---|--:|--:|--:|--:|--:|--:|"]
        for p in PROGRAMS:
            c = cells.get(p)
            if c is None:
                out.append(f"| {n[p]} | not in this run | | | | | | |")
                continue
            k = c["counts"]
            word, lost, gained = judge(base, c) if p != "wkhtmltopdf" else (c["state"], [], [])
            out.append(f"| {n[p]} | {word}: {c['why']} | {k['tests']} | {k['passed']} | {k['failed']} | {k['skipped']} | {c['calls']} | {c.get('seconds', '')} |")
        opts = sorted(set().union(*[set(c.get("options", [])) for c in cells.values() if c]))
        if opts:
            out += ["", "Options the library sent: " + ", ".join(f"`{o}`" for o in opts) + "."]
        for p in PROGRAMS:
            c = cells.get(p)
            if not c:
                continue
            if c["state"] == "did not run":
                out += ["", f"**{n[p]}** did not run: {c['why']} (steps: {', '.join(f'{k} {v}' for k, v in c.get('steps', {}).items())})."]
                continue
            bad = sorted((t, v[1]) for t, v in c["tests"].items() if v[0] == "fail")
            if not bad:
                continue
            out += ["", f"**Failed with {n[p]}:**", "", "| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |", "|---|---|---|---|"]
            for t, why in bad:
                b = (base or {}).get("tests", {}).get(t, ["not run"])[0] if p != "wkhtmltopdf" else "–"
                bw = {"pass": "passes", "fail": "fails too", "skip": "skipped"}.get(b, b)
                note = note_for(lib["key"], p, t, why) or ""
                out.append(f"| `{t}` | {bw} | {why.replace('|', '/') or '(no message)'} | {note} |")
        out.append("")
    return "\n".join(out) + "\n"


def best_pair(arch):
    """The pair of versions on file to show: the newest marqius-wkhtmltopdf, then the newest PDFKiln."""
    best = None
    for p in (ROOT / "results").glob(f"*/{arch}/results.json"):
        d = json.loads(p.read_text())
        k = (vkey(d["versions"]["marqius"]), vkey(d["versions"]["pdfkiln"]), d["date"])
        if best is None or k > best[0]:
            best = (k, d)
    return best[1] if best else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts")
    ap.add_argument("programs")
    ap.add_argument("--summary")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--message")
    ap.add_argument("--subjects", help="write the SHA-256 of each file filed, for the attestation")
    a = ap.parse_args()
    libs = json.loads((ROOT / "libraries.json").read_text())["libraries"]
    programs = json.loads(Path(a.programs).read_text())
    cells = load_cells(a.artifacts)
    v = {f["program"]: f["version"] for f in programs["files"]}
    versions = {"marqius": v["marqius"], "pdfkiln": v["pdfkiln"], "wkhtmltopdf": v["wkhtmltopdf"]}
    versions["pair"] = f"marqius-wkhtmltopdf-{versions['marqius']}_pdfkiln-{versions['pdfkiln']}"
    run_url = os.environ.get("RUN_URL", "")
    date = datetime.datetime.now(datetime.timezone.utc).strftime("%-d %B %Y")
    archs = sorted({c["arch"] for c in cells})
    summary, filed, subjects = [], [], []
    for arch in archs:
        by = {}
        for c in cells:
            if c["arch"] == arch:
                by.setdefault(c["library"], {})[c["program"]] = c
        ran = [lib for lib in libs if lib["key"] in by]
        summary.append(table(ran, by, versions, run_url, arch, date).replace(START, "").replace(END, ""))
        if a.dry_run:
            continue
        if len(ran) < len(libs):
            print(f"{arch}: {len(ran)} of {len(libs)} libraries in this run; a run of some libraries is shown in its summary, not filed")
            continue
        d = ROOT / "results" / versions["pair"] / arch
        d.mkdir(parents=True, exist_ok=True)
        data = {"date": date, "run_url": run_url, "arch": arch, "versions": versions, "programs": programs,
                "libraries": ran, "cells": [c for c in cells if c["arch"] == arch]}
        (d / "results.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
        (d / "report.md").write_text(report(ran, by, versions, programs, run_url, arch, date))
        subjects += [d / "results.json", d / "report.md"]
        hist = ROOT / "results" / "history.tsv"
        rows = hist.read_text().splitlines() if hist.exists() else ["date\tarch\tmarqius-wkhtmltopdf\tpdfkiln\tlibraries\tmarqius keeps up\tpdfkiln keeps up\trun"]
        k = {p: sum(judge(by[x["key"]].get("wkhtmltopdf"), by[x["key"]].get(p))[0] == "keeps up" for x in ran) for p in ("marqius", "pdfkiln")}
        rows.append("\t".join([date, arch, versions["marqius"], versions["pdfkiln"], str(len(ran)), str(k["marqius"]), str(k["pdfkiln"]), run_url]))
        hist.write_text("\n".join(rows) + "\n")
        filed.append(f"{versions['pair']} ({arch})")
    if a.summary:
        with open(a.summary, "a") as f:
            f.write("\n".join(summary) + "\n")
    if a.dry_run:
        print("\n".join(summary))
        return
    # the README shows the newest pair on file, on x86-64 (and says where ARM64's is)
    show = best_pair("x86-64") or best_pair("arm64")
    if show:
        by = {}
        for c in show["cells"]:
            by.setdefault(c["library"], {})[c["program"]] = c
        twin = ROOT / "results" / show["versions"]["pair"] / ("arm64" if show["arch"] == "x86-64" else "x86-64") / "results.json"
        other = json.loads(twin.read_text()) if twin.exists() else None
        block = table(show["libraries"], by, show["versions"], show["run_url"], show["arch"], show["date"], other)
        repo = os.environ.get("REPOSITORY", "")
        if os.environ.get("ATTESTED") == "true" and repo:
            path = f"results/{show['versions']['pair']}/{show['arch']}/results.json"
            check = ["", "**Check these results.** Each run's files are attested by the run that made them. With the GitHub CLI, signed in:", "",
                     "```bash", f"git clone https://github.com/{repo}.git", f"cd {repo.split('/')[-1]}",
                     f"gh attestation verify {path} -R {repo}", "```", "",
                     "It shows the workflow, the commit and the run that made the file."]
            block = block.replace("\n" + END, "\n".join(check) + "\n\n" + END)
        readme = ROOT / "README.md"
        text = readme.read_text()
        if START in text and END in text:
            text = text[: text.index(START)] + block + text[text.index(END) + len(END):]
            readme.write_text(text)
    if a.message and filed:
        Path(a.message).write_text(f"Results for {', '.join(filed)}\n\nFrom {run_url}\n")
    if a.subjects and subjects:
        import hashlib
        subjects.append(ROOT / "results" / "history.tsv")   # every file this run wrote under results/
        Path(a.subjects).write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT)}\n" for p in subjects))


if __name__ == "__main__":
    main()
