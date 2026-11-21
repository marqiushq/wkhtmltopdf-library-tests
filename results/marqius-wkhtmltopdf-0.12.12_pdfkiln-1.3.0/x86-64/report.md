# Library test suites: marqius-wkhtmltopdf 0.12.12 and PDFKiln 1.3.0, with wkhtmltopdf 0.12.6

Run of 21 November 2026 on GitHub's Ubuntu 24.04 machines (x86-64): https://github.com/marqiushq/wkhtmltopdf-library-tests/actions/runs/44886681397

## The programs

| Program | File | SHA-256 | Checked against | Provenance attestation | Says (`wkhtmltopdf -V`) |
|---|---|---|---|---|---|
| wkhtmltopdf 0.12.6 | [wkhtmltox_0.12.6.1-3.jammy_amd64.deb](https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_amd64.deb) | `4f723b2691ad8638…` | programs.json | none published (2023, before attestations) | `wkhtmltopdf 0.12.6.1 (with patched qt)` |
| marqius-wkhtmltopdf 0.12.12 | [marqius-wkhtmltopdf-linux-x86_64](https://marqius.com/download/marqius-wkhtmltopdf/0.12.12/marqius-wkhtmltopdf-linux-x86_64) | `0d178c26f1244072…` | https://marqius.com/download/marqius-wkhtmltopdf/0.12.12/marqius-wkhtmltopdf-linux-x86_64.sha256 | verified: signed by https://github.com/marqiushq/marqius-wkhtmltopdf/.github/workflows/release.yml@refs/heads/main, https://github.com/marqiushq/marqius-wkhtmltopdf/actions/runs/44873448543/attempts/1 | `wkhtmltopdf 0.12.6 (with patched qt) (compatible; marqius-wkhtmltopdf 0.12.12)` |
| PDFKiln 1.3.0 | [pdfkiln_1.3.0-1_amd64.deb](https://github.com/pdfkiln/pdfkiln/releases/download/1.3.0/pdfkiln_1.3.0-1_amd64.deb) | `1dacf9cdd7195a53…` | the release's SHA256SUMS | verified: signed by https://github.com/pdfkiln/pdfkiln/.github/workflows/ci.yml@refs/heads/main, https://github.com/pdfkiln/pdfkiln/actions/runs/44286283706/attempts/1 | `wkhtmltopdf 0.12.6 (with patched qt), pdfkiln 1.3.0, Chromium 158.0.8127.36` |

## The libraries

### python-pdfkit 1.0.0 (Python)

[JazzCore/python-pdfkit at c7c609f](https://github.com/JazzCore/python-pdfkit/tree/c7c609f46512f40e3bd6009bcb17bc1201316753), run as its CI runs it: `nosetests -w tests`. Python 3.9.25, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.376.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 47 passed, 0 skipped | 47 | 47 | 0 | 0 | 9 | 1 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 47 passed, 0 skipped | 47 | 47 | 0 | 0 | 9 | 0 |
| PDFKiln 1.3.0 | keeps up: 47 passed, 0 skipped | 47 | 47 | 0 | 0 | 9 | 2 |

Options the library sent: `--bad-option`, `--cookie`, `--footer-line`, `--outline`, `--page-size`, `--quiet`.

### imgkit V1.2.3 (Python)

[jarrekk/imgkit at 3ee9977](https://github.com/jarrekk/imgkit/tree/3ee9977004a7ad24aaa71890f4591ce646d0b95e), run as its CI runs it: `nosetests --where tests imgkit_test.py`. Python 3.9.25, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.133.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 48 passed, 0 skipped | 48 | 48 | 0 | 0 | 9 | 3 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 48 passed, 0 skipped | 48 | 48 | 0 | 0 | 9 | 24 |
| PDFKiln 1.3.0 | keeps up: 48 passed, 0 skipped | 48 | 48 | 0 | 0 | 9 | 5 |

Options the library sent: `--bad-option`, `--format`.

### django-wkhtmltopdf v3.4.0 (Python)

[incuna/django-wkhtmltopdf at 8a73477](https://github.com/incuna/django-wkhtmltopdf/tree/8a73477c7f2051bcc463fc8e7a2fdd7fec6d17fc), run as its CI runs it: `make test (python wkhtmltopdf/tests/run.py), Django 4.0`. Python 3.9.25, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.133.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | failed: 4 of 18 tests failed | 18 | 14 | 4 | 0 | 14 | 4 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 4 of 18 tests failed | 18 | 14 | 4 | 0 | 14 | 1 |
| PDFKiln 1.3.0 | behind: 7 of 18 tests failed | 18 | 11 | 7 | 0 | 12 | 5 |

Options the library sent: `--encoding`, `--footer-html`, `--quiet`, `--title`.

**Failed with wkhtmltopdf 0.12.6:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_response` | – | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdfrdvx50hn.html', '--quiet', '--title', 'Test PDF', '/tmp/wkhtmltopdf273achyu.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_response_to_browser` | – | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdfw1klfqeu.html', '--quiet', '--title', 'Test PDF', '/tmp/wkhtmltopdflip7b1hg.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_view` | – | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdfbp0jm_na.html', '--quiet', '/tmp/wkhtmltopdf35vfj2d4.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_view_to_browser` | – | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdfjukmqm0n.html', '--quiet', '/tmp/wkhtmltopdf9jjy733i.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |

**Failed with marqius-wkhtmltopdf 0.12.12:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_response` | fails too | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdfuis3qpjm.html', '--quiet', '--title', 'Test PDF', '/tmp/wkhtmltopdfb_e27x_6.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_response_to_browser` | fails too | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdfhvs0xmlj.html', '--quiet', '--title', 'Test PDF', '/tmp/wkhtmltopdfjdfe4vko.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_view` | fails too | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdf0ga9wtkk.html', '--quiet', '/tmp/wkhtmltopdfsrydkt2r.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_view_to_browser` | fails too | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdfn63p1txp.html', '--quiet', '/tmp/wkhtmltopdfg6qofx28.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |

**Failed with PDFKiln 1.3.0:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `wkhtmltopdf.tests.tests.TestUtils::test_render_with_null_request` | passes | self.assertTrue(pdf_content.endswith(b'%%EOF\n')): AssertionError: False is not true | How a PDF ends: the tests check that the PDF ends with “%%EOF” and a line break, as wkhtmltopdf's PDFs do; PDFKiln's PDFs end without the line break. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_response` | fails too | self.assertTrue(pdf_content.endswith(b'%%EOF\n')): AssertionError: False is not true | How a PDF ends: the tests check that the PDF ends with “%%EOF” and a line break, as wkhtmltopdf's PDFs do; PDFKiln's PDFs end without the line break. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_response_to_browser` | fails too | self.assertTrue(pdf_content.endswith(b'%%EOF\n')): AssertionError: False is not true | How a PDF ends: the tests check that the PDF ends with “%%EOF” and a line break, as wkhtmltopdf's PDFs do; PDFKiln's PDFs end without the line break. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_view` | fails too | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdfybt99w9v.html', '--quiet', '/tmp/wkhtmltopdfy4896rg0.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_view_to_browser` | fails too | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdf3aatmd2z.html', '--quiet', '/tmp/wkhtmltopdfmd6ezlfk.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_view_unicode` | passes | self.assertTrue(response.content.endswith(b'%%EOF\n')): AssertionError: False is not true | How a PDF ends: the tests check that the PDF ends with “%%EOF” and a line break, as wkhtmltopdf's PDFs do; PDFKiln's PDFs end without the line break. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_view_unicode_to_browser` | passes | self.assertTrue(response.content.endswith(b'%%EOF\n')): AssertionError: False is not true | How a PDF ends: the tests check that the PDF ends with “%%EOF” and a line break, as wkhtmltopdf's PDFs do; PDFKiln's PDFs end without the line break. |

### Snappy v1.7.3 (PHP)

[KnpLabs/snappy at f749a7d](https://github.com/KnpLabs/snappy/tree/f749a7d2e0f1260f4a0f96925323e34ede898f1f), run as its CI runs it: `vendor/bin/phpunit`. PHP 8.4.28, Composer version 2.11.2 2026-11-10 10:09:37, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.133.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 49 passed, 0 skipped | 49 | 49 | 0 | 0 | 0 | 0 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 49 passed, 0 skipped | 49 | 49 | 0 | 0 | 0 | 0 |
| PDFKiln 1.3.0 | keeps up: 49 passed, 0 skipped | 49 | 49 | 0 | 0 | 0 | 0 |

### laravel-snappy v1.0.5 (PHP)

[barryvdh/laravel-snappy at d702a7b](https://github.com/barryvdh/laravel-snappy/tree/d702a7b712b63027d5bf5ad321afd84996305a2b), run as its CI runs it: `composer test (phpunit), Laravel 13`. PHP 8.4.28, Composer version 2.11.2 2026-11-10 10:09:37, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.133.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 6 passed, 0 skipped | 6 | 6 | 0 | 0 | 5 | 1 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 6 passed, 0 skipped | 6 | 6 | 0 | 0 | 5 | 0 |
| PDFKiln 1.3.0 | keeps up: 6 passed, 0 skipped | 6 | 6 | 0 | 0 | 5 | 2 |

Options the library sent: `--lowquality`.

### phpwkhtmltopdf 2.5.0 (PHP)

[mikehaertl/phpwkhtmltopdf at 17ee713](https://github.com/mikehaertl/phpwkhtmltopdf/tree/17ee71341591415d942774eda2c98d8ba7ea9e90), run as its CI runs it: `vendor/bin/phpunit`. PHP 8.0.30, Composer version 2.11.2 2026-11-10 10:09:37, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.133.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 34 passed, 0 skipped | 34 | 34 | 0 | 0 | 34 | 12 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 34 passed, 0 skipped | 34 | 34 | 0 | 0 | 34 | 1 |
| PDFKiln 1.3.0 | keeps up: 34 passed, 0 skipped | 34 | 34 | 0 | 0 | 34 | 12 |

Options the library sent: `--allow`, `--cookie`, `--disable-dotted-lines`, `--footer-html`, `--header-center`, `--header-html`, `--margin-top`, `--no-background`, `--no-outline`, `--replace`, `--transparent`, `--width`, `--zoom`.

### KnpSnappyBundle v1.10.6 (PHP, Symfony)

[KnpLabs/KnpSnappyBundle at 9501e76](https://github.com/KnpLabs/KnpSnappyBundle/tree/9501e76b63158bc6c390065ede40963d5a94b065), run as its CI runs it: `vendor/bin/phpunit`. PHP 8.4.28, Composer version 2.11.2 2026-11-10 10:09:37, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.376.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 26 passed, 0 skipped | 26 | 26 | 0 | 0 | 0 | 1 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 26 passed, 0 skipped | 26 | 26 | 0 | 0 | 0 | 0 |
| PDFKiln 1.3.0 | keeps up: 26 passed, 0 skipped | 26 | 26 | 0 | 0 | 0 | 1 |

### CakePdf 5.3.0 (PHP, CakePHP)

[FriendsOfCake/CakePdf at 9c478eb](https://github.com/FriendsOfCake/CakePdf/tree/9c478eba9fa697513b5fd7ec69cdf0a37d81869c), run as its CI runs it: `vendor/bin/phpunit`. PHP 8.4.28, Composer version 2.11.2 2026-11-10 10:09:37, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.133.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 33 passed, 1 skipped | 34 | 33 | 0 | 1 | 0 | 0 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 33 passed, 1 skipped | 34 | 33 | 0 | 1 | 0 | 0 |
| PDFKiln 1.3.0 | keeps up: 33 passed, 1 skipped | 34 | 33 | 0 | 1 | 0 | 1 |

### wicked_pdf 2.7.0 (Ruby, Rails)

[mileszs/wicked_pdf at edcd80e](https://github.com/mileszs/wicked_pdf/tree/edcd80e7a96b5fe79476f7984e5ff8f3765f220d), run as its CI runs it: `bundle exec rake setup_and_run_tests, Rails 7.0`. ruby 3.2.11, Bundler version 2.4.19, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.376.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 45 passed, 0 skipped | 45 | 45 | 0 | 0 | 8 | 3 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 45 passed, 0 skipped | 45 | 45 | 0 | 0 | 8 | 2 |
| PDFKiln 1.3.0 | keeps up: 45 passed, 0 skipped | 45 | 45 | 0 | 0 | 8 | 3 |

### PDFKit v0.8.7.3 (Ruby)

[pdfkit/pdfkit at 762b366](https://github.com/pdfkit/pdfkit/tree/762b366e9420f8d2b9fc50a372b51094a0247dd4), run as its CI runs it: `bundle exec rake (rspec), Rails 7.0`. ruby 3.1.7p261, Bundler version 2.3.27, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.133.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 180 passed, 2 skipped | 182 | 180 | 0 | 2 | 66 | 22 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 180 passed, 2 skipped | 182 | 180 | 0 | 2 | 69 | 2 |
| PDFKiln 1.3.0 | behind: 1 of 182 tests failed | 182 | 179 | 1 | 2 | 69 | 19 |

Options the library sent: `--disable-smart-shrinking`, `--encoding`, `--header-center`, `--header-spacing`, `--javascript-delay`, `--margin-bottom`, `--margin-left`, `--margin-right`, `--margin-top`, `--page-size`, `--quiet`.

**Failed with PDFKiln 1.3.0:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `./spec/pdfkit_spec.rb[1:4:14] PDFKit#to_pdf can handle ampersands in URLs` | passes | PDFKit::ImproperWkhtmltopdfExitStatus: Command failed (exitstatus=1): ["/usr/local/bin/wkhtmltopdf", "--disable-smart-shrinking", "--quiet", "--page-size", "Le … argin-right", "0.75in", "--margin-bottom", "0.75in", "--margin-left", "0.75in", "--encoding", "UTF-8", "https://www.google.com/search?q=pdfkit&sort=ASC", "-"] | Google's “unusual traffic” page: the test converts a Google search page; on these machines Google answers PDFKiln's request with that page, and PDFKiln stops with an error, while wkhtmltopdf 0.12.6 and marqius-wkhtmltopdf are sent the search page itself. |

### wkhtmltopdf for Node 0.4.0 (JavaScript)

[devongovett/node-wkhtmltopdf at 51745d8](https://github.com/devongovett/node-wkhtmltopdf/tree/51745d803a65134dd87c30fd3276ca48630e467d), run as its CI runs it: `npm test (jasmine)`. Node.js v22.23.5, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.133.1). Runtime: it has no CI of its own: Node 22, a long-term-support release.

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 5 passed, 0 skipped | 5 | 5 | 0 | 0 | 5 | 2 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 5 passed, 0 skipped | 5 | 5 | 0 | 0 | 5 | 0 |
| PDFKiln 1.3.0 | keeps up: 5 passed, 0 skipped | 5 | 5 | 0 | 0 | 5 | 2 |

Options the library sent: `--quiet`.

### go-wkhtmltopdf v1.9.3 (Go)

[SebastiaanKlippert/go-wkhtmltopdf at efe6a20](https://github.com/SebastiaanKlippert/go-wkhtmltopdf/tree/efe6a2047eb2c6bb25cced3b07f8ea4ebef516ba), run as its CI runs it: `go test -v`. go version go1.27.4 linux/amd64, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.133.1). Runtime: its CI takes the newest stable Go, which is 1.27.

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | failed: 2 of 34 tests failed | 34 | 31 | 2 | 1 | 16 | 16 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 2 of 34 tests failed | 34 | 31 | 2 | 1 | 16 | 39 |
| PDFKiln 1.3.0 | keeps up: 2 of 34 tests failed | 34 | 31 | 2 | 1 | 16 | 22 |

Options the library sent: `--allow`, `--custom-header`, `--disable-dotted-lines`, `--disable-smart-shrinking`, `--dpi`, `--enable-local-file-access`, `--footer-font-size`, `--footer-html`, `--footer-right`, `--footer-spacing`, `--grayscale`, `--header-spacing`, `--margin-bottom`, `--margin-left`, `--margin-right`, `--margin-top`, `--orientation`, `--page-height`, `--page-size`, `--page-width`, `--version`, `--viewport-size`, `--window-status`, `--xsl-style-sheet`, `--zoom`.

**Failed with wkhtmltopdf 0.12.6:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `github.com/SebastiaanKlippert/go-wkhtmltopdf TestGeneratePdfFromStdinHtml5` | – | Error: Failed to load https://loremflickr.com/480/480, with network status code 299 and http status code 500 - Error downloading https://loremflickr.com/480/480 - server replied: Internal Server Error | Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load. |
| `github.com/SebastiaanKlippert/go-wkhtmltopdf TestTOCAndCustomFooter` | – | Error: Failed to load https://loremflickr.com/480/480, with network status code 299 and http status code 500 - Error downloading https://loremflickr.com/480/480 - server replied: Internal Server Error | Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load. |

**Failed with marqius-wkhtmltopdf 0.12.12:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `github.com/SebastiaanKlippert/go-wkhtmltopdf TestGeneratePdfFromStdinHtml5` | fails too | Warning: Failed to load https://loremflickr.com/480/480, with network status code 203 and http status code 500 - 500 Internal Server Error | Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load. |
| `github.com/SebastiaanKlippert/go-wkhtmltopdf TestTOCAndCustomFooter` | fails too | Warning: Failed to load https://loremflickr.com/480/480, with network status code 203 and http status code 500 - 500 Internal Server Error | Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load. |

**Failed with PDFKiln 1.3.0:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `github.com/SebastiaanKlippert/go-wkhtmltopdf TestGeneratePdfFromStdinHtml5` | fails too | Error: Failed to load https://loremflickr.com/480/480, with network status code 299 and http status code 500 - Error downloading https://loremflickr.com/480/480 - server replied: Internal Server Error | Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load. |
| `github.com/SebastiaanKlippert/go-wkhtmltopdf TestTOCAndCustomFooter` | fails too | Error: Failed to load https://loremflickr.com/480/480, with network status code 299 and http status code 500 - Error downloading https://loremflickr.com/480/480 - server replied: Internal Server Error | Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load. |

### java-wkhtmltopdf-wrapper 1.3.1-RELEASE (Java)

[jhonnymertz/java-wkhtmltopdf-wrapper at 13c44f0](https://github.com/jhonnymertz/java-wkhtmltopdf-wrapper/tree/13c44f0743ef1e8b17b7e1716eb4cfd482e79f12), run as its CI runs it: `mvn --batch-mode --update-snapshots verify`. openjdk version "1.8.0_512", Apache Maven 3.10.1 (3afd8084b5629f80b97750906a719879ed4cd283), on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.376.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 30 passed, 0 skipped | 30 | 30 | 0 | 0 | 12 | 24 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 30 passed, 0 skipped | 30 | 30 | 0 | 0 | 13 | 16 |
| PDFKiln 1.3.0 | keeps up: 30 passed, 0 skipped | 30 | 30 | 0 | 0 | 13 | 27 |

Options the library sent: `--exclude-from-outline`, `--footer-center`, `--header-center`, `--javascript-delay`, `--toc-header-text`, `--window-status`.

### pdf_generator v0.6.2 (Elixir)

[gutschilla/elixir-pdf-generator at 9c4fa3b](https://github.com/gutschilla/elixir-pdf-generator/tree/9c4fa3b40f5c4d79f065a3a73bf33a5e7a5ad17f), run as its CI runs it: `mix test`. Elixir 1.16.3 (compiled with Erlang/OTP 26), OTP 26, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.133.1). Runtime: its CI ran Elixir 1.9 on Alpine; here Elixir 1.16 with OTP 26 on Ubuntu.

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | failed: 3 of 15 tests failed | 15 | 12 | 3 | 0 | 11 | 183 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 3 of 15 tests failed | 15 | 12 | 3 | 0 | 11 | 182 |
| PDFKiln 1.3.0 | keeps up: 5 of 15 tests failed | 15 | 10 | 5 | 0 | 9 | 184 |

Options the library sent: `--margin-right`, `--orientation`, `--page-size`.

**Failed with wkhtmltopdf 0.12.6:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `test chrome's no-sandbox option doesn't crash` | – | ** (ExUnit.TimeoutError) test timed out after 60000ms. You can change the timeout: | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |
| `test chrome-headless from URL (assuming google.com is up and running)` | – | ** (ExUnit.TimeoutError) test timed out after 60000ms. You can change the timeout: | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |
| `test chrome-headless from file` | – | ** (ExUnit.TimeoutError) test timed out after 60000ms. You can change the timeout: | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |

**Failed with marqius-wkhtmltopdf 0.12.12:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `test chrome's no-sandbox option doesn't crash` | fails too | ** (ExUnit.TimeoutError) test timed out after 60000ms. You can change the timeout: | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |
| `test chrome-headless from URL (assuming google.com is up and running)` | fails too | ** (ExUnit.TimeoutError) test timed out after 60000ms. You can change the timeout: | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |
| `test chrome-headless from file` | fails too | ** (ExUnit.TimeoutError) test timed out after 60000ms. You can change the timeout: | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |

**Failed with PDFKiln 1.3.0:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `test chrome's no-sandbox option doesn't crash` | fails too | ** (ExUnit.TimeoutError) test timed out after 60000ms. You can change the timeout: | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |
| `test chrome-headless from URL (assuming google.com is up and running)` | fails too | ** (ExUnit.TimeoutError) test timed out after 60000ms. You can change the timeout: | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |
| `test chrome-headless from file` | fails too | ** (ExUnit.TimeoutError) test timed out after 60000ms. You can change the timeout: | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |
| `test generate! with filename option returns custom filename` | passes | ** (ArgumentError) construction of binary failed: segment 2 of type 'binary': expected a binary but got: {:generator_failed, "xvfb-run: error: Xvfb failed to start\n"} | A virtual display that did not start: the library starts the program inside a virtual display (xvfb-run), which failed to start on this machine, so the program never ran in this test; it is shown, and not counted. |
| `test generate_binary reads file` | passes | ** (ExUnit.AssertionError) match (=) failed code:  assert {:ok, "%PDF-1" <> _pdf} = @html /> PdfGenerator.generate_binary() left:  {:ok, "%PDF-1" <> _pdf} right: {:error, {:generator_failed, "xvfb-run: error: Xvfb failed to start\n"}} | A virtual display that did not start: the library starts the program inside a virtual display (xvfb-run), which failed to start on this machine, so the program never ran in this test; it is shown, and not counted. |

### Rotativa.AspNetCore v1.5.0 (.NET)

[webgio/Rotativa.AspNetCore at 84c470e](https://github.com/webgio/Rotativa.AspNetCore/tree/84c470e82f2fec13e1d4755c86fee90a9606c3ac), run as its CI runs it: `build-demo.sh, then run-tests.sh (the demo app, then dotnet test against it)`. .NET SDK 11.0.100, on Ubuntu 24.04.5 LTS x86_64 (GitHub runner image ubuntu24 20261116.133.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 10 passed, 0 skipped | 10 | 10 | 0 | 0 | 4 | 25 |
| marqius-wkhtmltopdf 0.12.12 | keeps up: 10 passed, 0 skipped | 10 | 10 | 0 | 0 | 4 | 23 |
| PDFKiln 1.3.0 | keeps up: 10 passed, 0 skipped | 10 | 10 | 0 | 0 | 4 | 22 |

Options the library sent: `--quality`.

