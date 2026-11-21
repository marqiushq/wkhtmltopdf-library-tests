# wkhtmltopdf library tests

**Will your code still work if you replace wkhtmltopdf?** Most applications do not run wkhtmltopdf themselves: they call it through a library such as pdfkit, wicked_pdf, Snappy or Rotativa. Each of those libraries has its own test suite, written by its own maintainers. This repository runs 15 of those suites, unchanged, with three programs in wkhtmltopdf's place: wkhtmltopdf 0.12.6 itself, marqius-wkhtmltopdf and PDFKiln. Every number below comes from a run on GitHub's own machines, and every run's logs are public.

> marqius-wkhtmltopdf is a paid product of Simple AI LLC, which publishes these tests. PDFKiln is a free program from another publisher, with no connection to us: it is tested as released, installed the way its own documentation says. The harness is open (MIT). We publish the misses along with the matches. If anything here is unfair to either program, open an issue.

## The results

<!-- results:start -->

With **marqius-wkhtmltopdf 0.12.11**, every test that passes with wkhtmltopdf 0.12.6 also passes in **15 of 15** libraries. With **PDFKiln 1.3.0**, in **11 of 15**.

Run of 21 November 2026 on GitHub's Ubuntu 24.04 machines (x86-64): [the run and its logs](https://github.com/marqiushq/wkhtmltopdf-library-tests/actions/runs/44873633491), [every failure and its reason](results/marqius-wkhtmltopdf-0.12.11_pdfkiln-1.3.0/x86-64/report.md). On ARM64 machines ([run of 21 November 2026](https://github.com/marqiushq/wkhtmltopdf-library-tests/actions/runs/44873633491), [report](results/marqius-wkhtmltopdf-0.12.11_pdfkiln-1.3.0/arm64/report.md)): marqius-wkhtmltopdf 0.12.11 in 15 of 15, PDFKiln 1.3.0 in 13 of 15.

| Library | Language | Tests | Program runs | wkhtmltopdf 0.12.6 | marqius-wkhtmltopdf 0.12.11 | PDFKiln 1.3.0 |
|---|---|--:|--:|---|---|---|
| [python-pdfkit](https://github.com/JazzCore/python-pdfkit/tree/c7c609f46512f40e3bd6009bcb17bc1201316753) 1.0.0 | Python | 47 | 9 | 47 passed | ✓ 47 passed | ✓ 47 passed |
| [imgkit](https://github.com/jarrekk/imgkit/tree/3ee9977004a7ad24aaa71890f4591ce646d0b95e) 1.2.3 | Python | 48 | 9 | 48 passed | ✓ 48 passed | ✓ 48 passed |
| [django-wkhtmltopdf](https://github.com/incuna/django-wkhtmltopdf/tree/8a73477c7f2051bcc463fc8e7a2fdd7fec6d17fc) 3.4.0 | Python | 18 | 14 | 14 passed, 4 failed | ✓ 14 passed, 4 failed | ✗ 11 passed, 7 failed (3 tests that pass with wkhtmltopdf) |
| [Snappy](https://github.com/KnpLabs/snappy/tree/f749a7d2e0f1260f4a0f96925323e34ede898f1f) 1.7.3 | PHP | 49 | 0 | 49 passed | ✓ 49 passed | ✓ 49 passed |
| [laravel-snappy](https://github.com/barryvdh/laravel-snappy/tree/d702a7b712b63027d5bf5ad321afd84996305a2b) 1.0.5 | PHP | 6 | 5 | 6 passed | ✓ 6 passed | ✓ 6 passed |
| [phpwkhtmltopdf](https://github.com/mikehaertl/phpwkhtmltopdf/tree/17ee71341591415d942774eda2c98d8ba7ea9e90) 2.5.0 | PHP | 34 | 34 | 34 passed | ✓ 34 passed | ✓ 34 passed |
| [KnpSnappyBundle](https://github.com/KnpLabs/KnpSnappyBundle/tree/9501e76b63158bc6c390065ede40963d5a94b065) 1.10.6 | PHP, Symfony | 26 | 0 | 26 passed | ✓ 26 passed | ✓ 26 passed |
| [CakePdf](https://github.com/FriendsOfCake/CakePdf/tree/9c478eba9fa697513b5fd7ec69cdf0a37d81869c) 5.3.0 | PHP, CakePHP | 34 | 0 | 33 passed, 1 skipped | ✓ 33 passed, 1 skipped | ✓ 33 passed, 1 skipped |
| [wicked_pdf](https://github.com/mileszs/wicked_pdf/tree/edcd80e7a96b5fe79476f7984e5ff8f3765f220d) 2.7.0 | Ruby, Rails | 45 | 8 | 45 passed | ✓ 45 passed | ✓ 45 passed |
| [PDFKit](https://github.com/pdfkit/pdfkit/tree/762b366e9420f8d2b9fc50a372b51094a0247dd4) 0.8.7.3 | Ruby | 182 | 67 | 180 passed, 2 skipped | ✓ 180 passed, 2 skipped | ✗ 179 passed, 1 failed, 2 skipped (1 test that passes with wkhtmltopdf) |
| [wkhtmltopdf for Node](https://github.com/devongovett/node-wkhtmltopdf/tree/51745d803a65134dd87c30fd3276ca48630e467d) 0.4.0 | JavaScript | 5 | 5 | 5 passed | ✓ 5 passed | ✓ 5 passed |
| [go-wkhtmltopdf](https://github.com/SebastiaanKlippert/go-wkhtmltopdf/tree/efe6a2047eb2c6bb25cced3b07f8ea4ebef516ba) 1.9.3 | Go | 34 | 16 | 31 passed, 2 failed, 1 skipped | ✓ 31 passed, 2 failed, 1 skipped | ✗ 27 passed, 6 failed, 1 skipped (4 tests that pass with wkhtmltopdf) |
| [java-wkhtmltopdf-wrapper](https://github.com/jhonnymertz/java-wkhtmltopdf-wrapper/tree/13c44f0743ef1e8b17b7e1716eb4cfd482e79f12) 1.3.1-RELEASE | Java | 30 | 13 | 30 passed | ✓ 30 passed | ✓ 30 passed |
| [pdf_generator](https://github.com/gutschilla/elixir-pdf-generator/tree/9c4fa3b40f5c4d79f065a3a73bf33a5e7a5ad17f) 0.6.2 | Elixir | 15 | 11 | 13 passed, 2 failed | ✓ 13 passed, 2 failed | ✗ 11 passed, 4 failed (1 test that passes with wkhtmltopdf) |
| [Rotativa.AspNetCore](https://github.com/webgio/Rotativa.AspNetCore/tree/84c470e82f2fec13e1d4755c86fee90a9606c3ac) 1.5.0 | .NET | 10 | 4 | 10 passed | ✓ 10 passed | ✓ 10 passed |

✓ every test that passes with wkhtmltopdf 0.12.6 passes with this program too. ✗ some do not: the number in brackets. The figures are what each test runner reported; a test that fails with wkhtmltopdf 0.12.6 too, or that drives another program instead of wkhtmltopdf (marked “not counted” below), is not held against either program. Program runs: how many times the suite started wkhtmltopdf or wkhtmltoimage.

Snappy, KnpSnappyBundle, CakePdf: their tests never start the program. They check the library's own code (the command it builds, its settings), so they pass whatever program is installed, or none.

**What fails, and why.** Failures that wkhtmltopdf 0.12.6 has too come first: they are not held against either program.

- **django-wkhtmltopdf**, 2 tests, with all three programs. A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that.
- **go-wkhtmltopdf**, 1 test, with all three programs. Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load.
- **pdf_generator**, 3 tests, not counted. Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted.
- **django-wkhtmltopdf**, 2 tests, with wkhtmltopdf 0.12.6 and marqius-wkhtmltopdf 0.12.11. A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that.
- **go-wkhtmltopdf**, 1 test, with wkhtmltopdf 0.12.6 and marqius-wkhtmltopdf 0.12.11. Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load.
- **django-wkhtmltopdf**, 5 tests, with PDFKiln 1.3.0. How a PDF ends: the tests check that the PDF ends with “%%EOF” and a line break, as wkhtmltopdf's PDFs do; PDFKiln's PDFs end without the line break.
- **PDFKit**, 1 test, with PDFKiln 1.3.0. Google's “unusual traffic” page: the test converts a Google search page; on these machines Google answers PDFKiln's request with that page, and PDFKiln stops with an error, while wkhtmltopdf 0.12.6 and marqius-wkhtmltopdf are sent the search page itself.
- **go-wkhtmltopdf**, 4 tests, with PDFKiln 1.3.0. The test runner says: “[>                                                           ] 0%”
- **go-wkhtmltopdf**, 1 test, with PDFKiln 1.3.0. The test runner says: “Error: Failed to load http://www.google.com/sorry/index?continue=http://www.google.com/&q=EgQDKp2BGObrhNgGIilK-CqpSxw5pAzdowcoOfVUaUSfvKykxVe5KimrF6YKZIsfE-KTS … =http://www.google.com/&q=EgQDKp2BGObrhNgGIilK-CqpSxw5pAzdowcoOfVUaUSfvKykxVe5KimrF6YKZIsfE-KTSQcDTTICclJaAUNgmYGxuJrlv_BF - server replied: Too Many Requests”
- **pdf_generator**, 1 test, with PDFKiln 1.3.0. The test runner says: “** (ArgumentError) construction of binary failed: segment 2 of type 'binary': expected a binary but got: {:generator_failed, "xvfb-run: error: Xvfb failed to start\n"}”

**Check these results.** Each run's files are attested by the run that made them. With the GitHub CLI, signed in:

```bash
git clone https://github.com/marqiushq/wkhtmltopdf-library-tests.git
cd wkhtmltopdf-library-tests
gh attestation verify results/marqius-wkhtmltopdf-0.12.11_pdfkiln-1.3.0/x86-64/results.json -R marqiushq/wkhtmltopdf-library-tests
```

It shows the workflow, the commit and the run that made the file.

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
