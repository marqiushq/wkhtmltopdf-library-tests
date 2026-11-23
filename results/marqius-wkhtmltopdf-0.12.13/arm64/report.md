# Library test suites: marqius-wkhtmltopdf 0.12.13, with wkhtmltopdf 0.12.6

Run of 23 November 2026 on GitHub's Ubuntu 24.04 machines (arm64): https://github.com/marqiushq/wkhtmltopdf-library-tests/actions/runs/45126128775

## The programs

| Program | File | SHA-256 | Checked against | Provenance attestation | Says (`wkhtmltopdf -V`) |
|---|---|---|---|---|---|
| wkhtmltopdf 0.12.6 | [wkhtmltox_0.12.6.1-3.jammy_arm64.deb](https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_arm64.deb) | `2095f20256661ebf…` | programs.json | none published (2023, before attestations) | `wkhtmltopdf 0.12.6.1 (with patched qt)` |
| marqius-wkhtmltopdf 0.12.13 | [marqius-wkhtmltopdf-linux-arm64](https://marqius.com/download/marqius-wkhtmltopdf/0.12.13/marqius-wkhtmltopdf-linux-arm64) | `cde19b5ca4b67849…` | https://marqius.com/download/marqius-wkhtmltopdf/0.12.13/marqius-wkhtmltopdf-linux-arm64.sha256 | verified: signed by https://github.com/marqiushq/marqius-wkhtmltopdf/.github/workflows/release.yml@refs/heads/main, https://github.com/marqiushq/marqius-wkhtmltopdf/actions/runs/44923927938/attempts/1 | `wkhtmltopdf 0.12.6 (with patched qt) (compatible; marqius-wkhtmltopdf 0.12.13)` |

## The libraries

### python-pdfkit 1.0.0 (Python)

[JazzCore/python-pdfkit at c7c609f](https://github.com/JazzCore/python-pdfkit/tree/c7c609f46512f40e3bd6009bcb17bc1201316753), run as its CI runs it: `nosetests -w tests`. Python 3.9.25, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 47 passed, 0 skipped | 47 | 47 | 0 | 0 | 9 | 2 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 47 passed, 0 skipped | 47 | 47 | 0 | 0 | 9 | 0 |

Options the library sent: `--bad-option`, `--cookie`, `--footer-line`, `--outline`, `--page-size`, `--quiet`.

### imgkit V1.2.3 (Python)

[jarrekk/imgkit at 3ee9977](https://github.com/jarrekk/imgkit/tree/3ee9977004a7ad24aaa71890f4591ce646d0b95e), run as its CI runs it: `nosetests --where tests imgkit_test.py`. Python 3.9.25, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 48 passed, 0 skipped | 48 | 48 | 0 | 0 | 9 | 3 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 48 passed, 0 skipped | 48 | 48 | 0 | 0 | 9 | 13 |

Options the library sent: `--bad-option`, `--format`.

### django-wkhtmltopdf v3.4.0 (Python)

[incuna/django-wkhtmltopdf at 8a73477](https://github.com/incuna/django-wkhtmltopdf/tree/8a73477c7f2051bcc463fc8e7a2fdd7fec6d17fc), run as its CI runs it: `make test (python wkhtmltopdf/tests/run.py), Django 4.0`. Python 3.9.25, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | failed: 4 of 18 tests failed | 18 | 14 | 4 | 0 | 14 | 4 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 4 of 18 tests failed | 18 | 14 | 4 | 0 | 14 | 1 |

Options the library sent: `--encoding`, `--footer-html`, `--quiet`, `--title`.

**Failed with wkhtmltopdf 0.12.6:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_response` | – | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdf9yt3_8nz.html', '--quiet', '--title', 'Test PDF', '/tmp/wkhtmltopdf_ou37x_1.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_response_to_browser` | – | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdf696o0i3i.html', '--quiet', '--title', 'Test PDF', '/tmp/wkhtmltopdfd7ivpnk2.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_view` | – | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdf34v_j4m7.html', '--quiet', '/tmp/wkhtmltopdfcdxg8uh5.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_view_to_browser` | – | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdf360lwe3e.html', '--quiet', '/tmp/wkhtmltopdfcnfto8o9.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |

**Failed with marqius-wkhtmltopdf 0.12.13:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_response` | fails too | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdf08mtfus3.html', '--quiet', '--title', 'Test PDF', '/tmp/wkhtmltopdfrfgpgoew.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_response_to_browser` | fails too | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdfofsl09z0.html', '--quiet', '--title', 'Test PDF', '/tmp/wkhtmltopdfkj721zi3.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_view` | fails too | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdfwfmqgodp.html', '--quiet', '/tmp/wkhtmltopdfxjgedunw.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |
| `wkhtmltopdf.tests.tests.TestViews::test_pdf_template_view_to_browser` | fails too | subprocess.CalledProcessError: Command '['/usr/local/bin/wkhtmltopdf', '--encoding', 'utf8', '--footer-html', '/tmp/wkhtmltopdfch6e1nrp.html', '--quiet', '/tmp/wkhtmltopdf8333agr2.html', '-']' returned non-zero exit status 1. | A footer with missing files: the test footer loads a script and a picture that do not exist, and wkhtmltopdf 0.12.6 stops with an error on that. |

### Snappy v1.7.3 (PHP)

[KnpLabs/snappy at f749a7d](https://github.com/KnpLabs/snappy/tree/f749a7d2e0f1260f4a0f96925323e34ede898f1f), run as its CI runs it: `vendor/bin/phpunit`. PHP 8.4.28, Composer version 2.11.2 2026-11-10 10:09:37, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 49 passed, 0 skipped | 49 | 49 | 0 | 0 | 0 | 0 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 49 passed, 0 skipped | 49 | 49 | 0 | 0 | 0 | 0 |

### laravel-snappy v1.0.5 (PHP)

[barryvdh/laravel-snappy at d702a7b](https://github.com/barryvdh/laravel-snappy/tree/d702a7b712b63027d5bf5ad321afd84996305a2b), run as its CI runs it: `composer test (phpunit), Laravel 13`. PHP 8.4.28, Composer version 2.11.2 2026-11-10 10:09:37, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 6 passed, 0 skipped | 6 | 6 | 0 | 0 | 5 | 2 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 6 passed, 0 skipped | 6 | 6 | 0 | 0 | 5 | 0 |

Options the library sent: `--lowquality`.

### phpwkhtmltopdf 2.5.0 (PHP)

[mikehaertl/phpwkhtmltopdf at 17ee713](https://github.com/mikehaertl/phpwkhtmltopdf/tree/17ee71341591415d942774eda2c98d8ba7ea9e90), run as its CI runs it: `vendor/bin/phpunit`. PHP 8.0.30, Composer version 2.11.2 2026-11-10 10:09:37, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 34 passed, 0 skipped | 34 | 34 | 0 | 0 | 34 | 12 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 34 passed, 0 skipped | 34 | 34 | 0 | 0 | 34 | 1 |

Options the library sent: `--allow`, `--cookie`, `--disable-dotted-lines`, `--footer-html`, `--header-center`, `--header-html`, `--margin-top`, `--no-background`, `--no-outline`, `--replace`, `--transparent`, `--width`, `--zoom`.

### KnpSnappyBundle v1.10.6 (PHP, Symfony)

[KnpLabs/KnpSnappyBundle at 9501e76](https://github.com/KnpLabs/KnpSnappyBundle/tree/9501e76b63158bc6c390065ede40963d5a94b065), run as its CI runs it: `vendor/bin/phpunit`. PHP 8.4.28, Composer version 2.11.2 2026-11-10 10:09:37, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 26 passed, 0 skipped | 26 | 26 | 0 | 0 | 0 | 0 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 26 passed, 0 skipped | 26 | 26 | 0 | 0 | 0 | 0 |

### CakePdf 5.3.0 (PHP, CakePHP)

[FriendsOfCake/CakePdf at 9c478eb](https://github.com/FriendsOfCake/CakePdf/tree/9c478eba9fa697513b5fd7ec69cdf0a37d81869c), run as its CI runs it: `vendor/bin/phpunit`. PHP 8.4.28, Composer version 2.11.2 2026-11-10 10:09:37, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 33 passed, 1 skipped | 34 | 33 | 0 | 1 | 0 | 0 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 33 passed, 1 skipped | 34 | 33 | 0 | 1 | 0 | 1 |

### wicked_pdf 2.7.0 (Ruby, Rails)

[mileszs/wicked_pdf at edcd80e](https://github.com/mileszs/wicked_pdf/tree/edcd80e7a96b5fe79476f7984e5ff8f3765f220d), run as its CI runs it: `bundle exec rake setup_and_run_tests, Rails 7.0`. ruby 3.2.11, Bundler version 2.4.19, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 45 passed, 0 skipped | 45 | 45 | 0 | 0 | 8 | 4 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 45 passed, 0 skipped | 45 | 45 | 0 | 0 | 8 | 2 |

### PDFKit v0.8.7.3 (Ruby)

[pdfkit/pdfkit at 762b366](https://github.com/pdfkit/pdfkit/tree/762b366e9420f8d2b9fc50a372b51094a0247dd4), run as its CI runs it: `bundle exec rake (rspec), Rails 7.0`. ruby 3.1.7p261, Bundler version 2.3.27, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 180 passed, 2 skipped | 182 | 180 | 0 | 2 | 72 | 23 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 180 passed, 2 skipped | 182 | 180 | 0 | 2 | 67 | 23 |

Options the library sent: `--disable-smart-shrinking`, `--encoding`, `--header-center`, `--header-spacing`, `--javascript-delay`, `--margin-bottom`, `--margin-left`, `--margin-right`, `--margin-top`, `--page-size`, `--quiet`.

### wkhtmltopdf for Node 0.4.0 (JavaScript)

[devongovett/node-wkhtmltopdf at 51745d8](https://github.com/devongovett/node-wkhtmltopdf/tree/51745d803a65134dd87c30fd3276ca48630e467d), run as its CI runs it: `npm test (jasmine)`. Node.js v22.23.5, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1). Runtime: it has no CI of its own: Node 22, a long-term-support release.

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 5 passed, 0 skipped | 5 | 5 | 0 | 0 | 5 | 2 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 5 passed, 0 skipped | 5 | 5 | 0 | 0 | 5 | 0 |

Options the library sent: `--quiet`.

### go-wkhtmltopdf v1.9.3 (Go)

[SebastiaanKlippert/go-wkhtmltopdf at efe6a20](https://github.com/SebastiaanKlippert/go-wkhtmltopdf/tree/efe6a2047eb2c6bb25cced3b07f8ea4ebef516ba), run as its CI runs it: `go test -v`. go version go1.27.4 linux/arm64, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1). Runtime: its CI takes the newest stable Go, which is 1.27.

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | failed: 2 of 35 tests failed | 35 | 32 | 2 | 1 | 16 | 20 |
| marqius-wkhtmltopdf 0.12.13 | behind: 2 of 34 tests failed | 34 | 31 | 2 | 1 | 16 | 17 |

Options the library sent: `--allow`, `--custom-header`, `--disable-dotted-lines`, `--disable-smart-shrinking`, `--dpi`, `--enable-local-file-access`, `--footer-font-size`, `--footer-html`, `--footer-right`, `--footer-spacing`, `--grayscale`, `--header-spacing`, `--margin-bottom`, `--margin-left`, `--margin-right`, `--margin-top`, `--orientation`, `--page-height`, `--page-size`, `--page-width`, `--version`, `--viewport-size`, `--window-status`, `--xsl-style-sheet`, `--zoom`.

**Failed with wkhtmltopdf 0.12.6:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `github.com/SebastiaanKlippert/go-wkhtmltopdf TestGeneratePdfFromStdinHtml5` | – | Error: Failed to load https://loremflickr.com/480/480, with network status code 299 and http status code 500 - Error downloading https://loremflickr.com/480/480 - server replied: Internal Server Error | Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load. |
| `github.com/SebastiaanKlippert/go-wkhtmltopdf TestTOCAndCustomFooter` | – | Error: Failed to load https://loremflickr.com/480/480, with network status code 299 and http status code 500 - Error downloading https://loremflickr.com/480/480 - server replied: Internal Server Error | Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load. |

**Failed with marqius-wkhtmltopdf 0.12.13:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `github.com/SebastiaanKlippert/go-wkhtmltopdf TestGeneratePdfFromStdinHtml5` | fails too | Error: Failed to load https://loremflickr.com/480/480, with network status code 299 and http status code 500 - Error downloading https://loremflickr.com/480/480 - server replied: Internal Server Error | Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load. |
| `github.com/SebastiaanKlippert/go-wkhtmltopdf TestTOCAndCustomFooter` | fails too | Error: Failed to load https://loremflickr.com/480/480, with network status code 299 and http status code 500 - Error downloading https://loremflickr.com/480/480 - server replied: Internal Server Error | Pictures from loremflickr.com: the test pages load pictures from loremflickr.com, which now answers with an error, and wkhtmltopdf 0.12.6 stops when a picture does not load. |

### java-wkhtmltopdf-wrapper 1.3.1-RELEASE (Java)

[jhonnymertz/java-wkhtmltopdf-wrapper at 13c44f0](https://github.com/jhonnymertz/java-wkhtmltopdf-wrapper/tree/13c44f0743ef1e8b17b7e1716eb4cfd482e79f12), run as its CI runs it: `mvn --batch-mode --update-snapshots verify`. openjdk version "1.8.0_512", Apache Maven 3.9.12 (848fbb4bf2d427b72bdb2471c22fced7ebd9a7a1), on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | passed: 30 passed, 0 skipped | 30 | 30 | 0 | 0 | 13 | 24 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 30 passed, 0 skipped | 30 | 30 | 0 | 0 | 13 | 16 |

Options the library sent: `--exclude-from-outline`, `--footer-center`, `--header-center`, `--javascript-delay`, `--toc-header-text`, `--window-status`.

### pdf_generator v0.6.2 (Elixir)

[gutschilla/elixir-pdf-generator at 9c4fa3b](https://github.com/gutschilla/elixir-pdf-generator/tree/9c4fa3b40f5c4d79f065a3a73bf33a5e7a5ad17f), run as its CI runs it: `mix test`. Elixir 1.16.3 (compiled with Erlang/OTP 26), OTP 26, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1). Runtime: its CI ran Elixir 1.9 on Alpine; here Elixir 1.16 with OTP 26 on Ubuntu.

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | failed: 3 of 15 tests failed | 15 | 12 | 3 | 0 | 11 | 4 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 3 of 15 tests failed | 15 | 12 | 3 | 0 | 11 | 1 |

Options the library sent: `--margin-right`, `--orientation`, `--page-size`.

**Failed with wkhtmltopdf 0.12.6:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `test chrome's no-sandbox option doesn't crash` | – | ** (FunctionClauseError) no function clause matching in IO.chardata_to_string/1 | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |
| `test chrome-headless from URL (assuming google.com is up and running)` | – | ** (ExUnit.AssertionError) Assertion with == failed code:  assert status == :ok left:  :error right: :ok | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |
| `test chrome-headless from file` | – | ** (MatchError) no match of right hand side value: {:error, {:generator_failed, "Error: Couldn't detect chrome version installed! use --chrome-binary to pass c … tests/wkhtmltopdf-library-tests/work/lib/priv/node_modules/chrome-headless-render-pdf/dist/index.js:689:39)\n    at tryCatch (/home/runner/work/wkhtmltopdf-li | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |

**Failed with marqius-wkhtmltopdf 0.12.13:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `test chrome's no-sandbox option doesn't crash` | fails too | ** (FunctionClauseError) no function clause matching in IO.chardata_to_string/1 | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |
| `test chrome-headless from URL (assuming google.com is up and running)` | fails too | ** (ExUnit.AssertionError) Assertion with == failed code:  assert status == :ok left:  :error right: :ok | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |
| `test chrome-headless from file` | fails too | ** (MatchError) no match of right hand side value: {:error, {:generator_failed, "Error: Couldn't detect chrome version installed! use --chrome-binary to pass c … tests/wkhtmltopdf-library-tests/work/lib/priv/node_modules/chrome-headless-render-pdf/dist/index.js:689:39)\n    at tryCatch (/home/runner/work/wkhtmltopdf-li | Chrome, not wkhtmltopdf: the library's tests of its Chrome option drive Google Chrome through its own Node helper, and on these machines they mostly do not finish within ExUnit's one-minute limit; they are shown, and not counted. |

### Rotativa.AspNetCore v1.5.0 (.NET)

[webgio/Rotativa.AspNetCore at 84c470e](https://github.com/webgio/Rotativa.AspNetCore/tree/84c470e82f2fec13e1d4755c86fee90a9606c3ac), run as its CI runs it: `build-demo.sh, then run-tests.sh (the demo app, then dotnet test against it)`. .NET SDK 11.0.100, on Ubuntu 24.04.5 LTS aarch64 (GitHub runner image ubuntu24-arm64 20261116.188.1).

| Program | Result | Tests | Passed | Failed | Skipped | Program runs | Seconds |
|---|---|--:|--:|--:|--:|--:|--:|
| wkhtmltopdf 0.12.6 | failed: 5 of 10 tests failed | 10 | 5 | 5 | 0 | 0 | 8 |
| marqius-wkhtmltopdf 0.12.13 | keeps up: 5 of 10 tests failed | 10 | 5 | 5 | 0 | 0 | 10 |

**Failed with wkhtmltopdf 0.12.6:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `can get a PDF with special characters(url: "http://localhost:5000", site: "Asp.net 10")` | – | OpenQA.Selenium.WebDriverException : Selenium Manager process exited abnormally with 65 code: /home/runner/work/wkhtmltopdf-library-tests/wkhtmltopdf-library-t … ebug/net10.0/runtimes/linux-arm64/native/selenium-manager  --browser "chrome" --browser-path "/usr/bin/google-chrome" --language-binding csharp --output mixed | No Chrome on ARM64: these tests open the demo application in Google Chrome through Selenium, which finds no Chrome on GitHub's ARM64 machines; they fail whichever program is installed. |
| `can get the PDF from the contact link(url: "http://localhost:5000", site: "Asp.net 10")` | – | OpenQA.Selenium.WebDriverException : Selenium Manager process exited abnormally with 65 code: /home/runner/work/wkhtmltopdf-library-tests/wkhtmltopdf-library-t … ebug/net10.0/runtimes/linux-arm64/native/selenium-manager  --browser "chrome" --browser-path "/usr/bin/google-chrome" --language-binding csharp --output mixed | No Chrome on ARM64: these tests open the demo application in Google Chrome through Selenium, which finds no Chrome on GitHub's ARM64 machines; they fail whichever program is installed. |
| `can get the jpg from the privacy image link(url: "http://localhost:5000", site: "Asp.net 10")` | – | OpenQA.Selenium.WebDriverException : Selenium Manager process exited abnormally with 65 code: /home/runner/work/wkhtmltopdf-library-tests/wkhtmltopdf-library-t … ebug/net10.0/runtimes/linux-arm64/native/selenium-manager  --browser "chrome" --browser-path "/usr/bin/google-chrome" --language-binding csharp --output mixed | No Chrome on ARM64: these tests open the demo application in Google Chrome through Selenium, which finds no Chrome on GitHub's ARM64 machines; they fail whichever program is installed. |
| `can get the png from the contact image link(url: "http://localhost:5000", site: "Asp.net 10")` | – | OpenQA.Selenium.WebDriverException : Selenium Manager process exited abnormally with 65 code: /home/runner/work/wkhtmltopdf-library-tests/wkhtmltopdf-library-t … ebug/net10.0/runtimes/linux-arm64/native/selenium-manager  --browser "chrome" --browser-path "/usr/bin/google-chrome" --language-binding csharp --output mixed | No Chrome on ARM64: these tests open the demo application in Google Chrome through Selenium, which finds no Chrome on GitHub's ARM64 machines; they fail whichever program is installed. |
| `should return the demo home page(url: "http://localhost:5000", site: "Asp.net 10")` | – | OpenQA.Selenium.WebDriverException : Selenium Manager process exited abnormally with 65 code: /home/runner/work/wkhtmltopdf-library-tests/wkhtmltopdf-library-t … ebug/net10.0/runtimes/linux-arm64/native/selenium-manager  --browser "chrome" --browser-path "/usr/bin/google-chrome" --language-binding csharp --output mixed | No Chrome on ARM64: these tests open the demo application in Google Chrome through Selenium, which finds no Chrome on GitHub's ARM64 machines; they fail whichever program is installed. |

**Failed with marqius-wkhtmltopdf 0.12.13:**

| Test | With wkhtmltopdf 0.12.6 | What the test runner says | Why |
|---|---|---|---|
| `can get a PDF with special characters(url: "http://localhost:5000", site: "Asp.net 10")` | fails too | OpenQA.Selenium.WebDriverException : Selenium Manager process exited abnormally with 65 code: /home/runner/work/wkhtmltopdf-library-tests/wkhtmltopdf-library-t … ebug/net10.0/runtimes/linux-arm64/native/selenium-manager  --browser "chrome" --browser-path "/usr/bin/google-chrome" --language-binding csharp --output mixed | No Chrome on ARM64: these tests open the demo application in Google Chrome through Selenium, which finds no Chrome on GitHub's ARM64 machines; they fail whichever program is installed. |
| `can get the PDF from the contact link(url: "http://localhost:5000", site: "Asp.net 10")` | fails too | OpenQA.Selenium.WebDriverException : Selenium Manager process exited abnormally with 65 code: /home/runner/work/wkhtmltopdf-library-tests/wkhtmltopdf-library-t … ebug/net10.0/runtimes/linux-arm64/native/selenium-manager  --browser "chrome" --browser-path "/usr/bin/google-chrome" --language-binding csharp --output mixed | No Chrome on ARM64: these tests open the demo application in Google Chrome through Selenium, which finds no Chrome on GitHub's ARM64 machines; they fail whichever program is installed. |
| `can get the jpg from the privacy image link(url: "http://localhost:5000", site: "Asp.net 10")` | fails too | OpenQA.Selenium.WebDriverException : Selenium Manager process exited abnormally with 65 code: /home/runner/work/wkhtmltopdf-library-tests/wkhtmltopdf-library-t … ebug/net10.0/runtimes/linux-arm64/native/selenium-manager  --browser "chrome" --browser-path "/usr/bin/google-chrome" --language-binding csharp --output mixed | No Chrome on ARM64: these tests open the demo application in Google Chrome through Selenium, which finds no Chrome on GitHub's ARM64 machines; they fail whichever program is installed. |
| `can get the png from the contact image link(url: "http://localhost:5000", site: "Asp.net 10")` | fails too | OpenQA.Selenium.WebDriverException : Selenium Manager process exited abnormally with 65 code: /home/runner/work/wkhtmltopdf-library-tests/wkhtmltopdf-library-t … ebug/net10.0/runtimes/linux-arm64/native/selenium-manager  --browser "chrome" --browser-path "/usr/bin/google-chrome" --language-binding csharp --output mixed | No Chrome on ARM64: these tests open the demo application in Google Chrome through Selenium, which finds no Chrome on GitHub's ARM64 machines; they fail whichever program is installed. |
| `should return the demo home page(url: "http://localhost:5000", site: "Asp.net 10")` | fails too | OpenQA.Selenium.WebDriverException : Selenium Manager process exited abnormally with 65 code: /home/runner/work/wkhtmltopdf-library-tests/wkhtmltopdf-library-t … ebug/net10.0/runtimes/linux-arm64/native/selenium-manager  --browser "chrome" --browser-path "/usr/bin/google-chrome" --language-binding csharp --output mixed | No Chrome on ARM64: these tests open the demo application in Google Chrome through Selenium, which finds no Chrome on GitHub's ARM64 machines; they fail whichever program is installed. |

