#!/usr/bin/env bash
# Downloads the three programs once for the whole run, checks each against its SHA-256 and, where
# its publisher makes one, its GitHub provenance attestation, and writes what it found to
# OUT/programs.json. Every cell then installs from these files, so all of them test the same bytes.
# Needs gh, with GH_TOKEN set, for the attestations.
#
#   bash harness/programs.sh MARQIUS_VERSION PDFKILN_VERSION "x86-64 arm64" OUT
set -euo pipefail
mq=$1 pk=$2 archs=$3 out=$4
here=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$out"
fetch() { curl -fsSL --retry 5 --retry-all-errors --retry-delay 5 --connect-timeout 20 -o "$2" "$1"; }
sha() { sha256sum "$1" | cut -c1-64; }
check() { # FILE EXPECTED WHAT
    local got
    got=$(sha "$1")
    if [ "$got" != "$2" ]; then echo "::error::$3: SHA-256 $got, expected $2" >&2; exit 1; fi
    echo "  $3: $(basename "$1") $got"
}
jq_prog() { jq -r --arg k "$1" --arg a "$2" --arg f "$3" '.programs[] | select(.key == $k) | .files[$a][$f]' "$here/programs.json"; }
# provenance FILE REPO WHAT: when REPO has a GitHub provenance attestation for this file's digest, it
# must verify (signed by a workflow of REPO) or nothing is tested; when it has none, the SHA-256 check
# above stands alone. Prints how the file was checked, for programs.json and the report.
provenance() {
    local file=$1 repo=$2 what=$3 digest n
    digest=$(sha "$file")
    if ! n=$(gh api "repos/$repo/attestations/sha256:$digest" --jq '.attestations | length' 2> "$out/attestation.err"); then
        if grep -q "HTTP 404" "$out/attestation.err"; then echo "none published"; return 0; fi
        echo "::error::$what: GitHub could not be asked for its attestations: $(cat "$out/attestation.err")" >&2
        return 1
    fi
    if [ "$n" = 0 ]; then echo "none published"; return 0; fi
    if ! gh attestation verify "$file" -R "$repo" --format json > "$out/attestation.json" 2> "$out/attestation.err"; then
        echo "::error::$what: $n attestation(s) found for $(basename "$file"), and none verifies: $(cat "$out/attestation.err")" >&2
        return 1
    fi
    jq -r '.[0].verificationResult.signature.certificate | "verified: signed by \(.buildSignerURI), \(.runInvocationURI)"' "$out/attestation.json"
}

echo "wkhtmltopdf 0.12.6, marqius-wkhtmltopdf $mq, PDFKiln $pk"
rows=()

# marqius-wkhtmltopdf: its installer, and its files laid out as on marqius.com, for MARQIUS_DOWNLOAD
fetch https://marqius.com/marqius-wkhtmltopdf.sh "$out/marqius-wkhtmltopdf.sh"
inst_sha=$(sha "$out/marqius-wkhtmltopdf.sh")
mkdir -p "$out/marqius/$mq"
echo "$mq" > "$out/marqius/latest"

# PDFKiln: the release's own list of SHA-256 sums
fetch "https://github.com/pdfkiln/pdfkiln/releases/download/$pk/SHA256SUMS" "$out/pdfkiln-SHA256SUMS"

for a in $archs; do
    # wkhtmltopdf 0.12.6: upstream's package, its SHA-256 kept in programs.json
    f=$(jq_prog wkhtmltopdf "$a" file)
    fetch "$(jq_prog wkhtmltopdf "$a" url)" "$out/$f"
    check "$out/$f" "$(jq_prog wkhtmltopdf "$a" sha256)" "wkhtmltopdf $a"
    rows+=("$(jq -n --arg p wkhtmltopdf --arg v 0.12.6.1-3 --arg a "$a" --arg f "$f" --arg s "$(sha "$out/$f")" \
        --arg u "$(jq_prog wkhtmltopdf "$a" url)" '{program:$p, version:$v, arch:$a, file:$f, sha256:$s, url:$u, checked:"programs.json", attestation:"none published (2023, before attestations)"}')")

    # marqius-wkhtmltopdf: the program and the .sha256 marqius.com publishes beside it
    f=$(jq_prog marqius "$a" file)
    u="https://marqius.com/download/marqius-wkhtmltopdf/$mq/$f"
    fetch "$u" "$out/marqius/$mq/$f"
    fetch "$u.sha256" "$out/marqius/$mq/$f.sha256"
    check "$out/marqius/$mq/$f" "$(cut -c1-64 "$out/marqius/$mq/$f.sha256")" "marqius-wkhtmltopdf $a"
    att=$(provenance "$out/marqius/$mq/$f" "$(jq -r '.programs[] | select(.key == "marqius") | .attestations' "$here/programs.json")" "marqius-wkhtmltopdf $a")
    echo "  marqius-wkhtmltopdf $a attestation: $att"
    rows+=("$(jq -n --arg p marqius --arg v "$mq" --arg a "$a" --arg f "$f" --arg s "$(sha "$out/marqius/$mq/$f")" \
        --arg u "$u" --arg t "$att" '{program:$p, version:$v, arch:$a, file:$f, sha256:$s, url:$u, checked:($u + ".sha256"), attestation:$t}')")

    # PDFKiln: its .deb, against the release's SHA256SUMS
    f=$(jq_prog pdfkiln "$a" file)
    f=${f//\{version\}/$pk}
    u="https://github.com/pdfkiln/pdfkiln/releases/download/$pk/$f"
    fetch "$u" "$out/$f"
    want=$(awk -v f="$f" '$2 == f || $2 == "*" f {print $1}' "$out/pdfkiln-SHA256SUMS")
    [ -n "$want" ] || { echo "::error::$f is not in PDFKiln $pk's SHA256SUMS" >&2; exit 1; }
    check "$out/$f" "$want" "PDFKiln $a"
    att=$(provenance "$out/$f" "$(jq -r '.programs[] | select(.key == "pdfkiln") | .attestations' "$here/programs.json")" "PDFKiln $a")
    echo "  PDFKiln $a attestation: $att"
    rows+=("$(jq -n --arg p pdfkiln --arg v "$pk" --arg a "$a" --arg f "$f" --arg s "$(sha "$out/$f")" \
        --arg u "$u" --arg t "$att" '{program:$p, version:$v, arch:$a, file:$f, sha256:$s, url:$u, checked:"the release'"'"'s SHA256SUMS", attestation:$t}')")
done

printf '%s\n' "${rows[@]}" | jq -s --arg i "$inst_sha" \
    '{files: ., installer: {url: "https://marqius.com/marqius-wkhtmltopdf.sh", sha256: $i}}' > "$out/programs.json"
echo "written: $out/programs.json"
