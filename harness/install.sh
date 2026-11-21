#!/usr/bin/env bash
# Installs one of the three programs the way its own documentation installs it, then puts a
# stand-in for wkhtmltopdf and wkhtmltoimage at /usr/local/bin, where upstream's package installs
# them and where libraries look. The stand-in notes each call a library makes, then becomes the
# program (exec), so the library talks to the program itself. A small page is converted first,
# to show the program works on this machine before any test runs.
#
#   bash harness/install.sh wkhtmltopdf|marqius|pdfkiln PROGRAMS_DIR ARCH
set -euo pipefail
prog=$1 arch=$3
dir=$(cd "$2" && pwd)
work=${WORK:-$PWD/work}
calls=/var/tmp/library-tests/calls
mkdir -p "$work/out"
f() { jq -r --arg p "$prog" --arg a "$arch" ".files[] | select(.program == \$p and .arch == \$a) | .$1" "$dir/programs.json"; }
file=$(f file)
version=$(f version)
[ -n "$file" ] && [ "$file" != null ] || { echo "::error::no $prog file for $arch in $dir/programs.json" >&2; exit 1; }

case $prog in
    wkhtmltopdf)
        # upstream's package installs both programs in /usr/local/bin; they move aside for the stand-ins
        sudo apt-get install -y "$dir/$file"
        sudo mkdir -p /opt/wkhtmltox/bin
        sudo mv /usr/local/bin/wkhtmltopdf /usr/local/bin/wkhtmltoimage /opt/wkhtmltox/bin/
        pdf=/opt/wkhtmltox/bin/wkhtmltopdf img=/opt/wkhtmltox/bin/wkhtmltoimage real=/opt/wkhtmltox/bin/wkhtmltopdf ;;
    marqius)
        # its one-line installer, given the version, reading the files checked by programs.sh
        sudo env MARQIUS_DOWNLOAD="file://$dir/marqius" bash "$dir/marqius-wkhtmltopdf.sh" --version "$version" --prefix /opt/marqius/bin
        pdf=/opt/marqius/bin/wkhtmltopdf img=/opt/marqius/bin/wkhtmltoimage real=/opt/marqius/bin/marqius-wkhtmltopdf
        got=$(sha256sum "$real" | cut -c1-64)
        [ "$got" = "$(f sha256)" ] || { echo "::error::installed marqius-wkhtmltopdf is $got, not the checked $(f sha256)" >&2; exit 1; }
        ;;
    pdfkiln)
        # its package, with what it recommends, as `apt install` does; its own links are
        # /usr/bin/wkhtmltopdf and wkhtmltoimage -> /usr/lib/pdfkiln/pdfkiln, which reads the name it was called by
        sudo apt-get install -y "$dir/$file"
        # one wkhtmltopdf per machine, at /usr/local/bin as with upstream's package: its links in
        # /usr/bin move aside (some libraries' tests count on finding the program in one place only)
        sudo mkdir -p /opt/pdfkiln-links
        sudo mv /usr/bin/wkhtmltopdf /usr/bin/wkhtmltoimage /opt/pdfkiln-links/
        pdf=/usr/lib/pdfkiln/pdfkiln img=/usr/lib/pdfkiln/pdfkiln real=/usr/lib/pdfkiln/pdfkiln ;;
    *) echo "::error::unknown program $prog" >&2; exit 1 ;;
esac

# /opt/under-test/bin/NAME: the program, called by its wkhtmltopdf name
sudo mkdir -p /opt/under-test/bin
sudo ln -sfn "$pdf" /opt/under-test/bin/wkhtmltopdf
sudo ln -sfn "$img" /opt/under-test/bin/wkhtmltoimage

# the stand-ins, where upstream's package puts wkhtmltopdf and where the libraries look
sudo mkdir -p "$calls"
sudo chmod 1777 /var/tmp/library-tests "$calls"
for name in wkhtmltopdf wkhtmltoimage; do
    for d in /usr/local/bin; do
        sudo rm -f "$d/$name"
        sudo tee "$d/$name" > /dev/null << EOF
#!/bin/sh
# Stands in for $name while a library's tests run: notes the call (its arguments, in a file of its
# own), then becomes the program under test, so its output, exit status and a library's kill on
# timeout all reach the program unchanged.
f=\$(mktemp $calls/call.XXXXXXXXXX 2> /dev/null) && printf '%s\\0' "$name" "\$@" > "\$f" 2> /dev/null
exec /opt/under-test/bin/$name "\$@"
EOF
        sudo chmod 755 "$d/$name"
    done
done

# nothing else answers to these names on this machine
for name in wkhtmltopdf wkhtmltoimage; do
    all=$(type -ap "$name" | tr '\n' ' ')
    [ "$all" = "/usr/local/bin/$name " ] || { echo "::error::$name is found at: $all" >&2; exit 1; }
done

# a page through each program, as a library would send it
tmp=$(mktemp -d)
printf '<!doctype html><html><head><meta charset="utf-8"><title>check</title></head><body><h1>Invoice 1001</h1><p>Total: 42.00</p></body></html>\n' > "$tmp/page.html"
v_pdf=$(wkhtmltopdf -V 2>&1 | head -n 3 | tr '\n' ' ')
v_img=$(wkhtmltoimage -V 2>&1 | head -n 3 | tr '\n' ' ')
wkhtmltopdf -q "$tmp/page.html" "$tmp/page.pdf"
wkhtmltoimage -q -f png "$tmp/page.html" "$tmp/page.png"
[ "$(head -c 5 "$tmp/page.pdf")" = "%PDF-" ] || { echo "::error::wkhtmltopdf made no PDF" >&2; exit 1; }
[ "$(head -c 4 "$tmp/page.png" | od -An -tx1 | tr -d ' \n')" = "89504e47" ] || { echo "::error::wkhtmltoimage made no PNG" >&2; exit 1; }
rm -rf "$tmp"
sudo find "$calls" -type f -delete

jq -n --arg p "$prog" --arg v "$version" --arg a "$arch" --arg f "$file" --arg s "$(sha256sum "$real" | cut -c1-64)" \
    --arg vp "$v_pdf" --arg vi "$v_img" \
    '{program:$p, version:$v, arch:$a, file:$f, program_sha256:$s, says_pdf:($vp|rtrimstr(" ")), says_image:($vi|rtrimstr(" "))}' > "$work/out/program.json"
echo "$prog $version ($arch) in place: wkhtmltopdf -V says: $v_pdf"
