# wkhtmltopdf library tests: will my library still work if I replace wkhtmltopdf?

**Your app probably doesn't run wkhtmltopdf itself.** It uses a library that runs it for you: pdfkit or django-wkhtmltopdf in Python, Snappy or laravel-snappy in PHP, wicked_pdf or PDFKit in Ruby, Rotativa in .NET, and others in Node.js, Go, Java and Elixir. Each of those libraries has its own test suite, written by its own authors.

**This repository runs 15 of those test suites, unchanged, with two programs in wkhtmltopdf's place:** the original wkhtmltopdf 0.12.6, and marqius-wkhtmltopdf, its maintained replacement. The rule is simple: every test that passes with wkhtmltopdf must also pass with marqius-wkhtmltopdf.

**Why it matters.** It answers "will my library still work after I switch?" with the library authors' own tests, not tests we wrote. Every run happens on GitHub's machines, in public, and every results file is signed by the run that made it, so nobody can quietly change a number.

> marqius-wkhtmltopdf is a paid product of Simple AI LLC, which publishes these tests. The harness is open (MIT). We publish the misses along with the matches. If anything here looks unfair to either program, open an issue.

Printing reports from Odoo or ERPNext? [wkhtmltopdf for Odoo and ERPNext](https://github.com/marqiushq/wkhtmltopdf-odoo-erpnext) prints their standard reports through their own Print buttons with the same two programs.

## The results

<!-- results:start -->

With **marqius-wkhtmltopdf 0.12.13**, every test that passes with wkhtmltopdf 0.12.6 also passes in **14 of 15** libraries.

Run of 23 November 2026 on GitHub's Ubuntu 24.04 machines (x86-64): [the run and its logs](https://github.com/marqiushq/wkhtmltopdf-library-tests/actions/runs/45126128775), [every failure and its reason](results/marqius-wkhtmltopdf-0.12.13/x86-64/report.md). On ARM64 machines ([run of 23 November 2026](https://github.com/marqiushq/wkhtmltopdf-library-tests/actions/runs/45126128775), [report](results/marqius-wkhtmltopdf-0.12.13/arm64/report.md)): marqius-wkhtmltopdf 0.12.13 in 14 of 15.

| Library | Language | Tests | Program runs | wkhtmltopdf 0.12.6 | marqius-wkhtmltopdf 0.12.13 |
|---|---|--:|--:|---|---|
| [python-pdfkit](https://github.com/JazzCore/python-pdfkit/tree/c7c609f46512f40e3bd6009bcb17bc1201316753) 1.0.0 | Python | 47 | 9 | 47 passed | ✓ 47 passed |
| [imgkit](https://github.com/jarrekk/imgkit/tree/3ee9977004a7ad24aaa71890f4591ce646d0b95e) 1.2.3 | Python | 48 | 9 | 48 passed | ✓ 48 passed |
| [django-wkhtmltopdf](https://github.com/incuna/django-wkhtmltopdf/tree/8a73477c7f2051bcc463fc8e7a2fdd7fec6d17fc) 3.4.0 | Python | 18 | 14 | 14 passed, 4 failed | ✓ 14 passed, 4 failed |
| [Snappy](https://github.com/KnpLabs/snappy/tree/f749a7d2e0f1260f4a0f96925323e34ede898f1f) 1.7.3 | PHP | 49 | 0 | 49 passed | ✓ 49 passed |
| [laravel-snappy](https://github.com/barryvdh/laravel-snappy/tree/d702a7b712b63027d5bf5ad321afd84996305a2b) 1.0.5 | PHP | 6 | 5 | 6 passed | ✓ 6 passed |
| [phpwkhtmltopdf](https://github.com/mikehaertl/phpwkhtmltopdf/tree/17ee71341591415d942774eda2c98d8ba7ea9e90) 2.5.0 | PHP | 34 | 34 | 34 passed | ✓ 34 passed |
| [KnpSnappyBundle](https://github.com/KnpLabs/KnpSnappyBundle/tree/9501e76b63158bc6c390065ede40963d5a94b065) 1.10.6 | PHP, Symfony | 26 | 0 | 26 passed | ✓ 26 passed |
| [CakePdf](https://github.com/FriendsOfCake/CakePdf/tree/9c478eba9fa697513b5fd7ec69cdf0a37d81869c) 5.3.0 | PHP, CakePHP | 34 | 0 | 33 passed, 1 skipped | ✓ 33 passed, 1 skipped |
| [wicked_pdf](https://github.com/mileszs/wicked_pdf/tree/edcd80e7a96b5fe79476f7984e5ff8f3765f220d) 2.7.0 | Ruby, Rails | 45 | 8 | 45 passed | ✓ 45 passed |
| [PDFKit](https://github.com/pdfkit/pdfkit/tree/762b366e9420f8d2b9fc50a372b51094a0247dd4) 0.8.7.3 | Ruby | 182 | 71 | 180 passed, 2 skipped | ✓ 180 passed, 2 skipped |
| [wkhtmltopdf for Node](https://github.com/devongovett/node-wkhtmltopdf/tree/51745d803a65134dd87c30fd3276ca48630e467d) 0.4.0 | JavaScript | 5 | 5 | 5 passed | ✓ 5 passed |
| [go-wkhtmltopdf](https://github.com/SebastiaanKlippert/go-wkhtmltopdf/tree/efe6a2047eb2c6bb25cced3b07f8ea4ebef516ba) 1.9.3 | Go | 35 | 16 | 32 passed, 2 failed, 1 skipped | ✗ 31 passed, 2 failed, 1 skipped (1 test that passes with wkhtmltopdf) |
| [java-wkhtmltopdf-wrapper](https://github.com/jhonnymertz/java-wkhtmltopdf-wrapper/tree/13c44f0743ef1e8b17b7e1716eb4cfd482e79f12) 1.3.1-RELEASE | Java | 30 | 13 | 30 passed | ✓ 30 passed |
| [pdf_generator](https://github.com/gutschilla/elixir-pdf-generator/tree/9c4fa3b40f5c4d79f065a3a73bf33a5e7a5ad17f) 0.6.2 | Elixir | 15 | 11 | 12 passed, 3 failed | ✓ 12 passed, 3 failed |
| [Rotativa.AspNetCore](https://github.com/webgio/Rotativa.AspNetCore/tree/84c470e82f2fec13e1d4755c86fee90a9606c3ac) 1.5.0 | .NET | 10 | 4 | 10 passed | ✓ 10 passed |

✓ every test that passes with wkhtmltopdf 0.12.6 passes with this program too. ✗ some do not: the number in brackets. The figures are what each test runner reported; a test that fails with wkhtmltopdf 0.12.6 too, or that drives another program instead of wkhtmltopdf (marked “not counted” below), is not held against either program. Program runs: how many times the suite started wkhtmltopdf or wkhtmltoimage.

Snappy, KnpSnappyBundle, CakePdf: their tests never start the program. They check the library's own code (the command it builds, its settings), so they pass whatever program is installed, or none.

**What fails, and why.** Failures that wkhtmltopdf 0.12.6 has too come first: they are not held against either program.

- **django-wkhtmltopdf**, 4 tests, with wkhtmltopdf 0.12.6 and marqius-wkhtmltopdf 0.12.13. A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that.
- **go-wkhtmltopdf**, 2 tests, with wkhtmltopdf 0.12.6 and marqius-wkhtmltopdf 0.12.13. Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load.
- **pdf_generator**, 3 tests, not counted. Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted.

**Check these results.** Each run's files are attested by the run that made them. With the GitHub CLI, signed in:

```bash
git clone https://github.com/marqiushq/wkhtmltopdf-library-tests.git
cd wkhtmltopdf-library-tests
gh attestation verify results/marqius-wkhtmltopdf-0.12.13/x86-64/results.json -R marqiushq/wkhtmltopdf-library-tests
```

It shows the workflow, the commit and the run that made the file.

<!-- results:end -->

## How each suite is run

- **The library's own tests, unchanged.** Each library is fetched from its own repository at the commit its release was made from. Its tests run the way its own CI runs them, with the runtime its CI used, or the nearest that still installs. No test is changed, skipped or run twice. Where the harness does more than the library's CI file, [`harness/suite.sh`](harness/suite.sh) says why: always to let the suite start on today's machines, never to make a test pass.
- **A fixed release of each library,** most at their latest release on GitHub. [`libraries.json`](libraries.json) lists each library with its commit and runtime.
- **One program per machine.** Each library runs twice on x86-64 and twice on ARM64, each time on a fresh GitHub machine (Ubuntu 24.04) with one program installed: wkhtmltopdf 0.12.6 from upstream's own package (0.12.6.1-3, with patched Qt), or marqius-wkhtmltopdf from its one-line installer. Every machine first gets the same system packages and fonts ([`harness/packages.txt`](harness/packages.txt)), so the program is the only difference.
- **The same files on every machine, checked.** One job downloads each program once and checks its SHA-256: against marqius.com's published sums, and against a sum kept in [`programs.json`](programs.json) for wkhtmltopdf. marqius-wkhtmltopdf's GitHub provenance attestation must verify too, or it is not tested. Each report lists the files and how each was checked.
- **Where libraries look.** On every machine, `wkhtmltopdf` and `wkhtmltoimage` are found in one place only, `/usr/local/bin`, where upstream's package installs them. What answers there is a small stand-in: it notes each call the library makes, then hands over to the program itself. The count of calls shows which suites start the program at all.
- **What counts.** A program keeps up with a library when every test that passes with wkhtmltopdf 0.12.6 passes with it too. Tests that fail with wkhtmltopdf itself, for example because a test page loads a picture from a website that now answers with an error, are listed with their reasons and not held against either program. Nor are tests that drive another program instead of wkhtmltopdf, such as pdf_generator's tests of its Chrome option: they are shown, marked "not counted".
- **Why a test fails.** Every failure is listed with what the test runner said. Where the cause is known, a note in plain words sits beside it ([`notes.tsv`](notes.tsv)). A note shows only while the failure it explains is still there.
- **When it runs.** Every day, when marqius-wkhtmltopdf has a version no run has tested; at each marqius-wkhtmltopdf release, the same day; every Monday, the latest versions again; and by hand. Each run files its results under [`results/`](results/) and rewrites the table above.
- **Signed results.** Every file a run files under [`results/`](results/) is attested by that run: anyone can check which workflow, commit and run made it, with the command under the table.

## Run it yourself

Fork this repository and run the **Libraries** workflow from the Actions tab. You can choose the versions, the libraries and the machines (x86-64, ARM64 or both), or leave them empty for the latest of everything on both. A full run is 60 jobs of one to eight minutes each. A run of some libraries only is reported on its own page, not filed.

## Questions

**Why do some libraries show no program runs?**
The tests of Snappy, KnpSnappyBundle and CakePdf check the command line the library builds, without starting the program. They pass with any program installed, or none. The "program runs" column shows how often each suite really started it.

**A test fails with wkhtmltopdf too. Is it held against marqius-wkhtmltopdf?**
No. Only tests that pass with wkhtmltopdf 0.12.6 count. Each failure is listed with the test runner's message and, where known, the reason.

**How do I know nobody edited these results?**
Each results file is signed by the GitHub run that made it. Check one with the `gh attestation verify` command under the table: it shows the workflow, the commit and the run.

**My library is not here. Can you add it?**
Open an issue with a link to its repository.

**How do I switch my own app?**
Point your library's wkhtmltopdf setting at marqius-wkhtmltopdf. The [examples](https://github.com/marqiushq/marqius-wkhtmltopdf-examples) show the one-line change for 14 libraries, and [marqius-wkhtmltopdf](https://github.com/marqiushq/marqius-wkhtmltopdf) shows how to install it.

## Licence

The harness is under the [MIT licence](LICENSE). Each library is fetched from its own repository when the tests run and keeps its own licence. marqius-wkhtmltopdf is proprietary software from Simple AI LLC, with a 30-day trial ([marqius.com](https://marqius.com)). wkhtmltopdf is under the LGPL. These tests are not affiliated with or endorsed by the wkhtmltopdf project or the libraries' maintainers.
