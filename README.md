# wkhtmltopdf library tests

**Will your code still work if you replace wkhtmltopdf?** Most applications do not run wkhtmltopdf themselves: they call it through a library such as pdfkit, wicked_pdf, Snappy or Rotativa. Each of those libraries has its own test suite, written by its own maintainers. This repository runs 15 of those suites, unchanged, with three programs in wkhtmltopdf's place: wkhtmltopdf 0.12.6 itself, marqius-wkhtmltopdf and PDFKiln. Every number below comes from a run on GitHub's own machines, and every run's logs are public.

> marqius-wkhtmltopdf is a paid product of Simple AI LLC, which publishes these tests. PDFKiln is a free program from another publisher, with no connection to us: it is tested as released, installed the way its own documentation says. The harness is open (MIT). We publish the misses along with the matches. If anything here is unfair to either program, open an issue.

## The results

<!-- results:start -->
The first run has not filed its results yet.
<!-- results:end -->

## How each suite is run

- **The suite is the library's own.** Each library is fetched from its own repository at the commit its release was made from, and its tests run as its own CI runs them, with the runtime its CI used, or the nearest that still installs ([`libraries.json`](libraries.json) says where). No test is changed, skipped or run twice. Where the harness does more than the library's CI file, [`harness/suite.sh`](harness/suite.sh) says why: always to let the suite start on today's machines, never to make a test pass.
- **Which releases.** Each library at its latest release on GitHub; for the seven that PDFKiln's README names, these are the versions it names. [`libraries.json`](libraries.json) lists each library with its commit and runtime.
- **One program per machine.** Each library runs three times on x86-64 and three times on ARM64, each time on a fresh GitHub machine (Ubuntu 24.04) with one program installed: wkhtmltopdf 0.12.6 from upstream's own package (0.12.6.1-3, with patched Qt), marqius-wkhtmltopdf from its one-line installer, PDFKiln from its Debian package. Every machine first gets the same system packages and fonts ([`harness/packages.txt`](harness/packages.txt)), so the program is the only difference.
- **The same files on every machine, checked.** One job downloads each program once and checks its SHA-256: against marqius.com's published sums, PDFKiln's `SHA256SUMS` and a sum kept in [`programs.json`](programs.json) for wkhtmltopdf. Where a publisher makes a GitHub provenance attestation for its file, that must verify too, or the program is not tested: PDFKiln's and marqius-wkhtmltopdf's releases carry one. Every machine installs those files, and each report lists them with how each was checked.
- **Where libraries look.** On every machine, `wkhtmltopdf` and `wkhtmltoimage` are found in one place only, `/usr/local/bin`, where upstream's package installs them and where the libraries look (PDFKiln's package also links them in `/usr/bin`; those links are moved aside). What answers there is a small stand-in: it notes each call the library makes, then hands over to the program itself, so the library talks to the program directly. The count of calls shows which suites start the program at all.
- **What counts.** A program keeps up with a library when every test that passes with wkhtmltopdf 0.12.6 passes with it too. Some tests fail with wkhtmltopdf 0.12.6 itself, for example where a test page loads pictures from a website that now answers with an error. They are listed with their reasons and not held against either program. Nor are tests that drive another program instead of wkhtmltopdf, such as pdf_generator's tests of its Chrome option: they are shown, marked “not counted”.
- **Why a test fails.** Every failure is listed with what the test runner said. Where the cause is known, a note in plain words sits beside it ([`notes.tsv`](notes.tsv)). A note shows only while the failure it explains is still there, so a fixed failure takes its note with it.
- **When it runs.** Every day, when either program has a version no run has tested; at each marqius-wkhtmltopdf release, the same day; every Monday, the latest versions again; and by hand. Each run files its results under [`results/`](results/) and writes the table above, so the versions shown are the ones tested.
- **Attested results.** The files a run files under [`results/`](results/) are attested by that run: anyone can check that a results file was made by this repository's workflow, and from which commit and in which run (the commands are under the table).

## Run it yourself

Fork this repository and run the **Libraries** workflow from the Actions tab. You can give the versions, the libraries and the machines (x86-64, ARM64 or both), or leave them empty for the latest of everything on both. A full run is 90 jobs of one to eight minutes each. A run of some libraries only is reported on its own page, not filed.

## Licence

The harness is under the [MIT licence](LICENSE). Each library is fetched from its own repository when the tests run and keeps its own licence. marqius-wkhtmltopdf is proprietary software from Simple AI LLC, with a 30-day trial ([marqius.com](https://marqius.com)). PDFKiln is published by its author under the MIT licence. wkhtmltopdf is under the LGPL. These tests are not affiliated with or endorsed by the wkhtmltopdf project, PDFKiln or the libraries' maintainers.
