#!/usr/bin/env bash
# One library's own test suite, in four steps, each a step of the GitHub job:
#
#   bash harness/suite.sh LIBRARY apt      the system packages: every cell's (packages.txt), then
#                                          what the library's own CI installs besides wkhtmltopdf
#   bash harness/suite.sh LIBRARY fetch    the library at its release, by commit (libraries.json)
#   bash harness/suite.sh LIBRARY deps     its dependencies, as its own CI installs them
#   bash harness/suite.sh LIBRARY test     its tests, as its own CI runs them, writing what the
#                                          test runner reports into work/out for results.py
#
# The tests themselves are never changed. Where a recipe does more than the library's CI file,
# the comment says why: always to let the suite start on today's machines, never to make a test pass.
set -uo pipefail
lib=$1 step=$2
here=$(cd "$(dirname "$0")/.." && pwd)
work=${WORK:-$PWD/work}
src=$work/lib
out=$work/out
mkdir -p "$work" "$out"
export DEBIAN_FRONTEND=noninteractive PIP_DISABLE_PIP_VERSION_CHECK=1 COMPOSER_NO_INTERACTION=1 \
    DOTNET_NOLOGO=1 DOTNET_CLI_TELEMETRY_OPTOUT=1 CI=true
L() { jq -r --arg k "$lib" ".libraries[] | select(.key == \$k) | $1" "$here/libraries.json"; }
[ -n "$(L .key)" ] || { echo "::error::unknown library $lib" >&2; exit 2; }

# retry N CMD...: for what fetches from the network (package managers), never for tests
retry() { local n=$1 i=1; shift; until "$@"; do [ $i -ge "$n" ] && return 1; echo "retrying ($i): $*" >&2; sleep $((i * 10)); i=$((i + 1)); done; }

# ---- the recipes: deps_KEY readies the library in $src; test_KEY runs its suite there

# python-pdfkit: its CI's ci/before-script.sh only installs wkhtmltopdf and what it needs
deps_python-pdfkit() { retry 3 pip install nose; }
test_python-pdfkit() { nosetests -v -w tests --with-xunit --xunit-file="$out/junit.xml"; }

# imgkit: its CI's commands (coverage left out: it measures the library's own code)
deps_imgkit() { retry 3 pip install six nose; }
test_imgkit() { nosetests -v --where tests imgkit_test.py --with-xunit --xunit-file="$out/junit.xml"; }

# django-wkhtmltopdf: `make test` is python wkhtmltopdf/tests/run.py, which names a test only
# when it fails; a copy at verbosity 2 names every one (the tests are the same). Its CI's Python
# had six, which the tests import.
deps_django-wkhtmltopdf() { retry 3 pip install "Django>=4.0,<4.1" six -r test_requirements.txt . ; }
test_django-wkhtmltopdf() {
    sed 's/verbosity=1/verbosity=2/' wkhtmltopdf/tests/run.py > wkhtmltopdf/tests/run_verbose.py
    WKHTMLTOPDF_CMD=/usr/local/bin/wkhtmltopdf python wkhtmltopdf/tests/run_verbose.py 2>&1 | tee "$out/unittest.txt"
    return "${PIPESTATUS[0]}"
}

# PHP: Composer from setup-php; PHPUnit writes JUnit
composer_update() { retry 3 composer update --prefer-dist --no-interaction --no-progress "$@"; }
test_phpunit() { vendor/bin/phpunit --log-junit "$out/junit.xml"; }
deps_snappy() { composer_update --no-security-blocking; }
test_snappy() { test_phpunit; }
deps_laravel-snappy() { composer require "laravel/framework:13.*" --no-update --no-progress && composer_update --prefer-stable; }
test_laravel-snappy() { test_phpunit; }
deps_phpwkhtmltopdf() { composer_update --optimize-autoloader; }
test_phpwkhtmltopdf() { test_phpunit; }
deps_knpsnappybundle() { composer_update --no-security-blocking; }
test_knpsnappybundle() { test_phpunit; }
deps_cakepdf() { composer_update; }
test_cakepdf() { test_phpunit; }

# wicked_pdf: Rails 7.0, the newest its CI ran, pointed at the program with WKHTMLTOPDF_BIN as its
# CI does (there at the distribution's /usr/bin/wkhtmltopdf). Rails 7.0 starts only with logger loaded first
# (RUBYOPT=-rlogger, for today's concurrent-ruby) and with minitest older than 5.25; the default
# task also runs RuboCop, a style check of its own code, left out
wicked_env() { export RUBYOPT=-rlogger BUNDLE_GEMFILE="$src/gemfiles/7.0.gemfile" WKHTMLTOPDF_BIN=/usr/local/bin/wkhtmltopdf; }
deps_wicked_pdf() {
    wicked_env
    printf "\ngem 'minitest', '~> 5.24.0'\n" >> gemfiles/7.0.gemfile
    # the Rails application its tests run in, made by its own Rakefile (setup_and_run_tests would
    # make it on the first run; made here, the test step times the tests alone)
    retry 3 bundle install --jobs 4 && bundle exec rake dummy_generate && [ -f test/dummy/config/environment.rb ]
}
test_wicked_pdf() {
    wicked_env
    bundle exec rake setup_and_run_tests TESTOPTS=-v 2>&1 | tee "$out/minitest.txt"
    return "${PIPESTATUS[0]}"
}

# PDFKit: Ruby 3.1 with Rails 7.0, its CI's newest pair; `rake` is rspec, here writing JSON too
pdfkit_env() { export RUBYOPT=-rlogger RAILS_VERSION='~> 7.0.0'; }
deps_pdfkit-ruby() { pdfkit_env && retry 3 bundle install --jobs 4; }
test_pdfkit-ruby() { pdfkit_env && bundle exec rspec --format progress --format json --out "$out/rspec.json"; }

# wkhtmltopdf for Node: `npm test` is jasmine; run through its own jasmine with a reporter added
# from outside the library, which writes each spec's result
deps_node() { retry 3 npm install --no-audit --no-fund; }
test_node() { MQ_RESULTS="$out/tests.jsonl" node "$here/harness/jasmine-run.js"; }

# go-wkhtmltopdf: its CI's `go test -v`, as JSON; its benchmarks (-bench) are timings, not tests
deps_go-wkhtmltopdf() { retry 3 go build ./...; }
test_go-wkhtmltopdf() { go test -v -count=1 -timeout 15m -json ./... > "$out/go.json"; }

# java-wkhtmltopdf-wrapper: its CI's Maven command; the tests' reports are read whether they pass
# or fail, and failures do not stop Maven before the integration tests
deps_java() { retry 3 mvn --batch-mode --update-snapshots -q -DskipTests install; }
test_java() {
    mvn --batch-mode --update-snapshots verify -Dmaven.test.failure.ignore=true 2>&1 | tee "$out/maven.txt"
    local s=${PIPESTATUS[0]}
    mkdir -p "$out/junit"
    cp target/surefire-reports/*.xml target/failsafe-reports/*.xml "$out/junit/" 2> /dev/null
    return "$s"
}

# pdf_generator: its CI's commands, and its `mix test` with ExUnit's own time limit of a minute a
# test. Its Chrome tests run its own priv/node_modules against the Google Chrome on GitHub's
# machines (its CI, on Alpine, skipped puppeteer's download for Alpine's Chromium; the global
# install its CI also made is for an option no test uses)
deps_pdf_generator() {
    export MIX_ENV=test PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true PUPPETEER_SKIP_DOWNLOAD=true
    retry 3 mix local.hex --force && retry 3 mix local.rebar --force && retry 3 mix deps.get &&
        (cd priv && retry 3 npm install --no-audit --no-fund) && mix compile
}
test_pdf_generator() {
    export MIX_ENV=test
    MQ_RESULTS="$out/tests.jsonl" elixir -r "$here/harness/exunit_formatter.exs" -S mix test \
        --formatter ExUnit.CLIFormatter --formatter LibraryTests.Formatter 2>&1 | tee "$out/exunit.txt"
    return "${PIPESTATUS[0]}"
}

# Rotativa.AspNetCore: its own build-demo.sh, the program linked where the demo app looks for it
# (as its test Dockerfile does), then run-tests.sh's three commands, with a TRX report added
rotativa_env() { export ROTATIVA_DEMO_URL=http://localhost:5000 ROTATIVA_CHROME_BINARY=/usr/bin/google-chrome; }
deps_rotativa() { rotativa_env && retry 3 bash Rotativa.AspNetCore.Tests/build-demo.sh; }
test_rotativa() {
    rotativa_env
    mkdir -p Rotativa.AspNetCore.DemoApp/wwwroot/Rotativa
    ln -sf /usr/local/bin/wkhtmltopdf Rotativa.AspNetCore.DemoApp/wwwroot/Rotativa/wkhtmltopdf
    ln -sf /usr/local/bin/wkhtmltoimage Rotativa.AspNetCore.DemoApp/wwwroot/Rotativa/wkhtmltoimage
    (cd Rotativa.AspNetCore.DemoApp && exec dotnet run --no-build --urls "$ROTATIVA_DEMO_URL") > "$out/app.txt" 2>&1 &
    local app=$! s
    for _ in $(seq 1 60); do curl -sf -o /dev/null "$ROTATIVA_DEMO_URL" && break; sleep 1; done
    dotnet test Rotativa.AspNetCore.Tests --no-build --logger "console;verbosity=normal" --logger "trx;LogFileName=$out/results.trx"
    s=$?
    kill $app 2> /dev/null
    wait $app 2> /dev/null
    return $s
}

case $step in
    apt)
        # --no-upgrade: what GitHub's machine has already stays as it is (installing libudev1 had
        # apt upgrade systemd, and rebuild the boot image, for up to twelve minutes on some machines).
        # Ubuntu's mirror once stalled a download for half an hour: each try is cut off after ten
        # minutes, and an interrupted dpkg is set right before the next one.
        mapfile -t pkgs < <(grep -v '^#' "$here/harness/packages.txt" | grep .)
        mapfile -t extra < <(L '.apt[]')
        apt_opts=(-q -o Acquire::http::Timeout=30 -o Acquire::https::Timeout=30 -o Acquire::Retries=3)
        apt_install() {
            sudo timeout 600 apt-get "${apt_opts[@]}" install -y --no-install-recommends --no-upgrade "$@" ||
                { sudo dpkg --configure -a > /dev/null 2>&1; return 1; }
        }
        retry 3 sudo timeout 600 apt-get "${apt_opts[@]}" update &&
            retry 3 apt_install "${pkgs[@]}" "${extra[@]}" ;;
    fetch)
        # the release's commit, with git (GitHub's archives can leave out the tests)
        rm -rf "$src" && mkdir -p "$src" && cd "$src" && git init -q . &&
            git remote add origin "https://github.com/$(L .repo).git" &&
            retry 3 git fetch -q --depth 1 origin "$(L .commit)" && git checkout -q FETCH_HEAD &&
            [ "$(git rev-parse HEAD)" = "$(L .commit)" ] &&
            echo "$(L .name) $(L .release) at $(git rev-parse HEAD)" ;;
    deps)
        cd "$src" && "deps_$lib" ;;
    test)
        (cd "$out" && rm -rf junit junit.xml rspec.json go.json tests.jsonl unittest.txt minitest.txt exunit.txt results.trx maven.txt app.txt)
        cd "$src" || exit 2
        # what this cell ran on: the runtime's version and the dependencies the library's tools resolved
        {
            echo "system: $(. /etc/os-release && echo "$PRETTY_NAME") $(uname -m)"
            echo "image: GitHub runner image ${ImageOS:-unknown} ${ImageVersion:-}"
            case $(L '.setup | keys[0]') in
                python) echo "runtime: $(python --version 2>&1)" ;;
                php) echo "runtime: $(php -r 'echo "PHP ", PHP_VERSION;'), $(composer --version 2> /dev/null | head -n 1)" ;;
                ruby) echo "runtime: $(ruby --version | cut -d' ' -f1-2), $(bundle --version)" ;;
                node) echo "runtime: Node.js $(node --version)" ;;
                go) echo "runtime: $(go version)" ;;
                java) echo "runtime: $(java -version 2>&1 | head -n 1), $(mvn --version 2> /dev/null | head -n 1)" ;;
                elixir) echo "runtime: $(elixir --version 2> /dev/null | tail -n 1), OTP $(erl -noshell -eval 'io:put_chars(erlang:system_info(otp_release)), halt().')" ;;
                dotnet) echo "runtime: .NET SDK $(dotnet --version)" ;;
            esac
        } > "$out/versions.txt" 2>&1
        for f in composer.lock Gemfile.lock gemfiles/7.0.gemfile.lock package-lock.json mix.lock go.sum; do
            [ -f "$f" ] && cp "$f" "$out/$(echo "$f" | tr / _)"
        done
        if command -v pip > /dev/null && [ "$(L '.setup | keys[0]')" = python ]; then pip freeze > "$out/pip-freeze.txt" 2> /dev/null; fi
        start=$(date +%s)
        "test_$lib"
        s=$?
        echo "$s $(($(date +%s) - start))" > "$work/test-status"
        exit $s ;;
    *) echo "::error::unknown step $step" >&2; exit 2 ;;
esac
