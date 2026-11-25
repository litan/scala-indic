#!/usr/bin/env bash
set -euo pipefail
kojo_hi_tools=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd -- "${1:-$kojo_hi_tools/../artifacts}"
kojo_hi_checksum=$(mktemp .SHA256SUMS.XXXXXX)
trap 'rm -f -- "$kojo_hi_checksum"' EXIT
sha256sum scala-library.jar scala-reflect.jar scala-compiler.jar scalariform.jar > "$kojo_hi_checksum"
mv -- "$kojo_hi_checksum" SHA256SUMS
