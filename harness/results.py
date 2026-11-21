#!/usr/bin/env python3
"""Reads what one cell's test runner reported, and the calls the stand-ins noted, into one file:

    python3 harness/results.py read LIBRARY PROGRAM ARCH > work/cell.json
    python3 harness/results.py verdict work/cell.json      exits 1 unless the suite passed

Each reader turns one runner's own report into {test: [status, reason]}, status pass, fail or
skip; the reason is the runner's own message for a failure, on one line. What the runner itself
says it ran is kept beside what the readers found, so that a reader that misses tests shows."""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = Path(os.environ.get("WORK", "work"))
OUT = WORK / "out"
CALLS = Path("/var/tmp/library-tests/calls")
INFO = {"--version", "-V", "--help", "-h", "-H", "--extended-help", "--readme", "--license", "--manpage", "--htmldoc"}


def one_line(text, n=320):
    """The first line of a message; a long one keeps its start and its end, where the point often is
    ("Process '<a long command>' timeout after 10 seconds")."""
    text = re.sub(r"\x1b\[[0-9;]*m", "", text or "")
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    s = lines[0] if lines else ""
    return s if len(s) <= n else s[: n // 2 - 1] + " … " + s[-(n // 2 - 2):]


def junit(p):
    """JUnit XML: nose, PHPUnit, Maven Surefire and Failsafe."""
    try:
        root = ET.parse(p).getroot()
    except (ET.ParseError, OSError):
        return {}
    r = {}
    for tc in root.iter("testcase"):
        cls = tc.get("classname") or tc.get("class") or tc.get("file") or ""
        name = f"{cls}::{tc.get('name', '')}".lstrip(":")
        bad = [c for c in tc if c.tag in ("failure", "error")]
        if bad:
            r[name] = ["fail", one_line(bad[0].get("message") or bad[0].text or bad[0].get("type", ""))]
        elif any(c.tag == "skipped" for c in tc):
            sk = next(c for c in tc if c.tag == "skipped")
            r[name] = ["skip", one_line(sk.get("message") or sk.text or "")]
        else:
            r[name] = ["pass", ""]
    return r


def rspec(p):
    """RSpec's JSON. An example is known by its id, its description beside it with numbers as #:
    RSpec writes computed values into descriptions (the size of that run's own PDF)."""
    try:
        examples = json.loads(p.read_text()).get("examples", [])
    except (ValueError, OSError):
        return {}
    m = {"passed": "pass", "failed": "fail", "pending": "skip"}
    r = {}
    for e in examples:
        name = f"{e.get('id', '')} {re.sub(r'[0-9]+', '#', e.get('full_description', ''))}".strip()
        ex = e.get("exception") or {}
        why = f"{ex.get('class', '')}: {ex.get('message', '')}" if ex else e.get("pending_message") or ""
        r[name] = [m.get(e.get("status"), "fail"), one_line(why)]
    return r


def go(p):
    """go test -json: a test's last pass, fail or skip is its result; its output gives the reason."""
    r, output = {}, {}
    for line in p.read_text(errors="replace").splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        t = e.get("Test")
        if not t:
            continue
        key = f"{e.get('Package', '')} {t}"
        if e.get("Action") == "output":
            output.setdefault(key, []).append(e.get("Output", ""))
        elif e.get("Action") in ("pass", "fail", "skip"):
            why = ""
            if e["Action"] == "fail":
                # go test -json cuts a long line into several pieces, and a progress bar redraws itself
                # with carriage returns, so the program's error can sit between two bars: join the
                # pieces back into the test's output, then split it at line ends and carriage returns
                lines = [y.strip() for y in re.split(r"[\r\n]+", "".join(output.get(key, [])))
                         if y.strip() and not y.strip().startswith(("=== ", "--- "))]
                # the program's own words first (wkhtmltopdf's "Error:", "Failed to load", "Exit with
                # code"), then the test's (testify's "Error:", a file:line message)
                prog = ([x for x in lines if x.startswith("Error:") and "Failed to load" in x]
                        or [x for x in lines if "Failed to load" in x or x.startswith("Exit with code")])
                err = [x for x in lines if x.startswith(("Error:", "Error Trace:"))]
                pick = [x for x in lines if re.match(r"^\w+_test\.go:\d+:", x)]
                why = one_line((prog or err or pick or lines or [""])[0])
            r[key] = [e["Action"], why]
    return r


def jsonl(p):
    """One JSON line a test, written by the reporters added from outside the library (jasmine, ExUnit)."""
    r = {}
    for line in p.read_text(errors="replace").splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        why = e.get("message", "")
        lines = [x.strip() for x in why.splitlines() if x.strip()]
        # a bare "** (ExUnit.AssertionError)" says what failed only in the lines after it
        if lines and re.fullmatch(r"\*\* \([\w.]+\)", lines[0]):
            why = " ".join(lines)
        r[e.get("name", "")] = [{"passed": "pass", "failed": "fail"}.get(e.get("status"), "skip"), one_line(why)]
    return r


UNITTEST_NAME = re.compile(r"^(test\w*) \(([\w.]+)\)")
UNITTEST_END = re.compile(r" \.\.\. (ok|FAIL|ERROR|skipped|expected failure|unexpected success)\b")
UNITTEST_ALONE = re.compile(r"^(ok|FAIL|ERROR|skipped\b.*|expected failure|unexpected success)$")
UNITTEST_BLOCK = re.compile(r"^(FAIL|ERROR): (test\w*) \(([\w.]+)\)")


def unittest(p):
    """unittest at verbosity 2: 'test_x (module.Class) ... ok'. What a test printed itself may come
    before its result, which then stands alone on a line. A failure's reason is the last line of
    its block (the exception)."""
    text = p.read_text(errors="replace")
    r, cur = {}, None
    for line in text.splitlines():
        m = UNITTEST_NAME.match(line)
        if m:
            cur = f"{m.group(2)}::{m.group(1)}"
        e = UNITTEST_END.search(line) or (UNITTEST_ALONE.match(line.strip()) if cur and not m else None)
        if e and cur:
            s = e.group(1)
            r[cur] = ["pass" if s in ("ok", "expected failure") else "skip" if s.startswith("skipped") else "fail", ""]
            cur = None
    blocks = re.split(r"^={50,}$", text, flags=re.M)
    for b in blocks:
        lines = b.strip().splitlines()
        if not lines:
            continue
        m = UNITTEST_BLOCK.match(lines[0])
        if m:
            # the traceback runs from the line of dashes under the name (and its docstring, at
            # verbosity 2) to the next such line
            body, inside = [], False
            for x in lines[1:]:
                if re.match(r"^-{50,}$", x):
                    if inside:
                        break
                    inside = True
                    continue
                if inside and x.strip():
                    body.append(x)
            key = f"{m.group(3)}::{m.group(2)}"
            why = body[-1] if body else m.group(1)
            # a bare "AssertionError: False is not true" says more beside the line that raised it
            if why.startswith("AssertionError") and len(body) > 1 and body[-2].startswith("    "):
                why = f"{body[-2].strip()}: {why}"
            r[key] = ["fail", one_line(why)]
    return r


MINITEST_LINE = re.compile(r"^([\w:]+#\S+) = [\d.]+ s = ([.FES])\s*$")
MINITEST_HEAD = re.compile(r"^\s*\d+\) (Failure|Error):\s*$")


def minitest(p):
    """Minitest with -v: 'Class#test_name = 0.12 s = .'; a failure's block gives its reason."""
    lines = p.read_text(errors="replace").splitlines()
    r = {}
    for line in lines:
        m = MINITEST_LINE.match(line)
        if m:
            r[m.group(1)] = [{".": "pass", "S": "skip"}.get(m.group(2), "fail"), ""]
    for i, line in enumerate(lines):
        if MINITEST_HEAD.match(line) and i + 1 < len(lines):
            name = re.split(r" \[|:$", lines[i + 1].strip())[0]
            why = next((x for x in lines[i + 2 : i + 8] if x.strip()), "")
            if name in r:
                r[name][1] = one_line(why)
    return r


EXUNIT_TEST = re.compile(r"^\s+\* (test .+) \(((?:\d+(?:\.\d+)?(?:ms|s))|skipped|excluded|invalid)\)(?: \[L#\d+\])?\s*$")
EXUNIT_FAIL = re.compile(r"^\s+\d+\) (test .+) \(([\w.]+)\)\s*$")


def exunit(p):
    """mix test --trace: '  * test name (1.2ms) [L#30]'; '  1) test name (Module)' then its reason."""
    lines = p.read_text(errors="replace").splitlines()
    r = {}
    for i, line in enumerate(lines):
        m = EXUNIT_TEST.match(line)
        if m:
            r.setdefault(m.group(1), ["skip" if m.group(2) in ("skipped", "excluded", "invalid") else "pass", ""])
        m = EXUNIT_FAIL.match(line)
        if m:
            body = [x.strip() for x in lines[i + 1 : i + 12] if x.strip()]
            body = [x for x in body if not re.match(r"^[\w/.-]+\.exs:\d+$", x)]
            r[m.group(1)] = ["fail", one_line(body[0] if body else "")]
    return r


def trx(p):
    """dotnet test's TRX."""
    try:
        root = ET.parse(p).getroot()
    except (ET.ParseError, OSError):
        return {}
    r = {}
    for e in root.iter():
        if e.tag.endswith("UnitTestResult"):
            o = e.get("outcome", "")
            msg = next((m.text for m in e.iter() if m.tag.endswith("Message") and m.text), "")
            r[e.get("testName", "")] = ["pass" if o == "Passed" else "skip" if o in ("NotExecuted", "Inconclusive") else "fail", one_line(msg)]
    return r


READERS = (("junit.xml", junit), ("junit/*.xml", junit), ("rspec.json", rspec), ("go.json", go),
           ("unittest.txt", unittest), ("minitest.txt", minitest), ("exunit.txt", exunit),
           ("tests.jsonl", jsonl), ("results.trx", trx))
SAYS = (("unittest.txt", re.compile(r"^Ran (\d+) tests? in", re.M)),
        ("exunit.txt", re.compile(r"\b(\d+) tests?, \d+ failures?")),
        ("minitest.txt", re.compile(r"^(\d+) runs, \d+ assertions", re.M)))


def tests_in(d):
    r = {}
    for pattern, read in READERS:
        for p in sorted(d.glob(pattern)):
            r.update(read(p))
    return r


def runner_says(d):
    """How many tests the runner itself says it ran, where it says so; None where none does."""
    total, said = 0, False
    for name, rx in SAYS:
        p = d / name
        m = rx.findall(p.read_text(errors="replace")) if p.exists() else []
        if m:
            total, said = total + int(m[-1]), True
    if (d / "rspec.json").exists():
        try:
            total, said = total + int(json.loads((d / "rspec.json").read_text())["summary"]["example_count"]), True
        except (ValueError, KeyError, OSError):
            pass
    for p in sorted(d.glob("junit.xml")) + sorted(d.glob("junit/*.xml")) + sorted(d.glob("results.trx")):
        try:
            root = ET.parse(p).getroot()
        except (ET.ParseError, OSError):
            continue
        if p.suffix == ".trx":
            c = next((e for e in root.iter() if e.tag.endswith("Counters")), None)
            n = int(c.get("total", 0)) if c is not None else None
        elif root.tag == "testsuites":
            n = sum(int(s.get("tests", 0)) for s in root.findall("testsuite"))
        else:
            n = int(root.get("tests", 0)) if root.get("tests") else None
        if n is not None:
            total, said = total + n, True
    return total if said else None


def calls():
    """The calls the stand-ins noted: [name, argument, ...] each."""
    r = []
    for p in sorted(CALLS.glob("call.*")) if CALLS.exists() else []:
        parts = p.read_bytes().decode("utf-8", "replace").split("\0")
        r.append([x for x in parts[:-1]] if parts and parts[-1] == "" else parts)
    return r


def read(library, program, arch):
    libs = {x["key"]: x for x in json.loads((ROOT / "libraries.json").read_text())["libraries"]}
    lib = libs[library]
    cell = {"library": library, "program": program, "arch": arch, "release": lib["release"], "commit": lib["commit"],
            "run_url": os.environ.get("RUN_URL", ""), "job": os.environ.get("JOB_TITLE", "")}
    pj = OUT / "program.json"
    cell["installed"] = json.loads(pj.read_text()) if pj.exists() else None
    steps = dict(x.split("=", 1) for x in os.environ.get("STEPS", "").split() if "=" in x)
    cell["steps"] = steps
    st = WORK / "test-status"
    if not st.exists():
        failed = next((k for k, v in steps.items() if v in ("failure", "cancelled")), None)
        why = ("the tests did not finish in the time allowed" if failed == "test"
               else f"the {failed} step did not finish" if failed else "the job stopped before the tests")
        cell.update(state="did not run", why=why)
        cell.update(tests={}, counts={"tests": 0, "passed": 0, "failed": 0, "skipped": 0}, runner_says=None, calls=0, conversions=0, options=[])
        return cell
    status, seconds = (WORK / "test-status").read_text().split()
    t = tests_in(OUT)
    counts = {"tests": len(t), "passed": sum(v[0] == "pass" for v in t.values()),
              "failed": sum(v[0] == "fail" for v in t.values()), "skipped": sum(v[0] == "skip" for v in t.values())}
    cs = calls()
    conv = [c for c in cs if any(a not in INFO for a in c[1:])]
    opts = sorted({a.split("=", 1)[0] for c in cs for a in c[1:] if a.startswith("--")})
    vt = OUT / "versions.txt"
    ran_on = dict(line.split(": ", 1) for line in vt.read_text().splitlines() if ": " in line) if vt.exists() else {}
    cell.update(tests=t, counts=counts, runner_says=runner_says(OUT), runner_status=int(status), seconds=int(seconds),
                calls=len(cs), conversions=len(conv), options=opts, ran_on=ran_on)
    if not t:
        cell.update(state="no results", why=f"the test runner ended with status {status} and reported no tests")
    elif counts["failed"]:
        cell.update(state="failed", why=f"{counts['failed']} of {counts['tests']} tests failed")
    elif int(status) != 0:
        cell.update(state="failed", why=f"no test failed, but the test runner ended with status {status}")
    else:
        cell.update(state="passed", why=f"{counts['passed']} passed, {counts['skipped']} skipped")
    return cell


def summary(cell):
    c = cell["counts"]
    inst = cell.get("installed") or {}
    lines = [f"### {cell.get('job') or cell['library']}", "",
             f"**{cell['state']}**: {cell['why']}." + (f" The program said: `{inst.get('says_pdf', '')}`." if inst else ""), ""]
    if cell["state"] != "did not run":
        lines.append(f"{c['tests']} tests: {c['passed']} passed, {c['failed']} failed, {c['skipped']} skipped"
                     + (f" (the runner says {cell['runner_says']})" if cell["runner_says"] is not None else "")
                     + f"; the library called the program {cell['calls']} times ({cell['conversions']} conversions).")
        bad = [(k, v[1]) for k, v in sorted(cell["tests"].items()) if v[0] == "fail"]
        if bad:
            lines += ["", "| Failed test | Reason |", "|---|---|"]
            lines += [f"| `{k}` | {why.replace('|', '/') or '(no message)'} |" for k, why in bad]
    return "\n".join(lines) + "\n"


def main():
    if sys.argv[1] == "read":
        cell = read(*sys.argv[2:5])
        print(json.dumps(cell, indent=1, ensure_ascii=False))
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
                f.write(summary(cell))
    elif sys.argv[1] == "verdict":
        cell = json.loads(Path(sys.argv[2]).read_text())
        for k, v in sorted(cell["tests"].items()):
            if v[0] == "fail":
                print(f"::error title={k[:120]}::{v[1] or 'failed'}")
        print(f"{cell['state']}: {cell['why']}")
        sys.exit(0 if cell["state"] == "passed" else 1)


if __name__ == "__main__":
    main()
