#!/bin/bash
# Collect lightweight style signals for a path and language.

set -euo pipefail

usage () {
    cat <<USAGE
Usage: $0 -l <language> -p <path>

Collect simple style signals to support manual review.
Languages: bash | python | go | typescript
USAGE
}

fail () {
    printf 'FAIL %s\n' "$*" >&2
    exit 2
}

lang=
root=

while getopts ':l:p:h' opt ; do
    case "${opt}" in
        l) lang="${OPTARG}" ;;
        p) root="${OPTARG}" ;;
        h) usage; exit 0 ;;
        :) fail "Option -${OPTARG} requires an argument" ;;
        \?) fail "Unknown option: -${OPTARG}" ;;
    esac
done

shift $((OPTIND - 1))
test $# -eq 0 || fail "Unexpected trailing arguments: $*"
test -n "${lang}" || fail "Missing -l <language>"
test -n "${root}" || fail "Missing -p <path>"
test -e "${root}" || fail "Path does not exist: ${root}"

case "${lang}" in
    bash)
        exts='*.sh'
        ;;
    python)
        exts='*.py'
        ;;
    go)
        exts='*.go'
        ;;
    typescript)
        exts='*.ts *.tsx'
        ;;
    *)
        fail "Unsupported language: ${lang}"
        ;;
esac

printf 'LANGUAGE: %s\n' "${lang}"
printf 'PATH: %s\n' "${root}"

for pattern in ${exts}; do
    find "${root}" -type f -name "${pattern}" 2>/dev/null
 done | sort -u | while read -r f; do
    test -n "${f}" || continue
    lines=$(wc -l < "${f}" | tr -d ' ')
    comments=$(grep -cE '^\s*(#|//|/\*|\*)' "${f}" || true)
    funcs=$(grep -cE '^\s*(function\s+|def\s+|func\s+|[A-Za-z0-9_]+\s*\()' "${f}" || true)
    printf '%s\tlines=%s\tcomments=%s\tfunc_like=%s\n' "${f}" "${lines}" "${comments}" "${funcs}"
done
