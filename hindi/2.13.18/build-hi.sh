#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
./scala/build-hi.sh
./scalariform/build-hi.sh
