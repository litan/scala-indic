# Build the Hindi Scala 2.13.18 toolchain

This recipe rebuilds Scala and Scalariform with five Hindi keyword aliases:
`मान` (`val`), `चर` (`var`), `परिभाषा` (`def`), `यदि` (`if`) and
`अन्यथा` (`else`). English keywords remain supported. Longer identifiers,
backquoted identifiers, comments and strings retain their usual behavior.

The repository stores patches and build tools. Upstream source trees, downloaded
tools, caches and build outputs live in a separate workspace.

## Pinned sources and tools

| Component | Upstream | Baseline commit | Modified version |
| --- | --- | --- | --- |
| Scala | <https://github.com/scala/scala.git> | `98f40d00ddcf59a802862d38a9fe79806cde59fa` (`v2.13.18`) | `2.13.18-bin-hi` |
| Scalariform | <https://github.com/bulent2k2/scalariform.git> | `8cf96a69d7a87a4b4d31a4061b8eb1ca615fd896` (before that fork's Turkish additions) | `0.2.10-hi` |

Both patches contain the complete difference from the corresponding baseline,
including tests, component build instructions, executable build/verification
scripts, and Scalariform's dedicated `hi-build/` definition. The component
`BUILD-HI.md` files are adapted from the original local checkouts to use this
recipe's portable workspace paths and log names; implementation, tests and
build scripts match the source commits below. Apply each patch once to its
unmodified baseline. These are Git diffs for `git apply`, not mail
patches for `git am`.

The source revisions in the local `kojo-scala-hi` checkouts and the expected
trees after applying these patches (including the adapted documentation) are:

| Component | Source commit | Patched Git tree |
| --- | --- | --- |
| Scala | `2b0a6fd1adb9cb3416029a51610445dbd242977a` | `5d659ffb40ea05888e88fe8cdfc810bb2c0bddd2` |
| Scalariform | `9cdfceec0e63e10ce1480f0b0b45e19af85daf11` | `1cfcf840a137187e5c254ceb895b74356f82fefc` |

The source commits are recorded for provenance; rebuilding only requires the
public upstream baselines and the patches in this directory. The tree IDs allow
verification of every patched file and its executable mode.

Use Linux with a Java 8 JDK, Bash, Git, curl, Python 3, `sha256sum`, and internet
access for uncached dependencies. The original build used AdoptOpenJDK
`1.8.0_265`. Both builds use sbt `1.11.7`. Scala bootstraps with upstream's
Scala `2.13.17`; the dedicated Scalariform build uses Scala `2.13.18`, targets
Java 8 bytecode, and pins scala-xml `1.2.0`, scala-parser-combinators `1.1.2`,
and ScalaTest `3.0.8`.

The shared launcher uses Maven Central and a workspace-specific sbt global
configuration. It defaults to Java on `PATH`, a 2 GB maximum heap and four
active processors. Optionally export `KOJO_HI_JAVA=/absolute/path/to/java`.

## Prepare a fresh workspace

From a checkout of `scala-indic`, run the following in one Bash session. The
workspace is newly created so these commands do not overwrite existing sources.
Record the printed path if you want to return to it later.

```bash
set -euo pipefail
cd hindi/2.13.18
recipe=$(pwd -P)
sha256sum -c SHA256SUMS
workspace=$(mktemp -d "${TMPDIR:-/tmp}/kojo-scala-hi.XXXXXXXX")
printf 'Build workspace: %s\n' "$workspace"

mkdir -p "$workspace/tools" "$workspace/logs"
cp "$recipe/README.md" "$recipe/build-hi.sh" "$workspace/"
cp "$recipe/tools/"* "$workspace/tools/"

git init "$workspace/scala"
git -C "$workspace/scala" remote add origin https://github.com/scala/scala.git
git -C "$workspace/scala" fetch --depth=1 origin 98f40d00ddcf59a802862d38a9fe79806cde59fa
git -C "$workspace/scala" checkout --detach 98f40d00ddcf59a802862d38a9fe79806cde59fa
git -C "$workspace/scala" apply --check --index "$recipe/scala.patch"
git -C "$workspace/scala" apply --index "$recipe/scala.patch"
test "$(git -C "$workspace/scala" write-tree)" = 5d659ffb40ea05888e88fe8cdfc810bb2c0bddd2

git init "$workspace/scalariform"
git -C "$workspace/scalariform" remote add origin https://github.com/bulent2k2/scalariform.git
git -C "$workspace/scalariform" fetch --depth=1 origin 8cf96a69d7a87a4b4d31a4061b8eb1ca615fd896
git -C "$workspace/scalariform" checkout --detach 8cf96a69d7a87a4b4d31a4061b8eb1ca615fd896
git -C "$workspace/scalariform" apply --check --index "$recipe/scalariform.patch"
git -C "$workspace/scalariform" apply --index "$recipe/scalariform.patch"
test "$(git -C "$workspace/scalariform" write-tree)" = 1cfcf840a137187e5c254ceb895b74356f82fefc

curl -fL https://repo.maven.apache.org/maven2/org/scala-sbt/sbt-launch/1.11.7/sbt-launch-1.11.7.jar \
  -o "$workspace/tools/sbt-launch.jar"
(
  cd "$workspace/tools"
  printf '%s  sbt-launch.jar\n' f92a2095ac75008764fe3b2b793ffe624c4fbef5bfd9b0022e4bc2daf668c651 | sha256sum -c -
)
```

The resulting layout matches the relative paths used by the build scripts:

```text
workspace/
  README.md       # this recipe, also linked from component build notes
  build-hi.sh
  scala/          # pinned upstream plus scala.patch
  scalariform/    # pinned upstream plus scalariform.patch
  tools/          # shared scripts, repository config and downloaded sbt launcher
  logs/
  artifacts/      # created by packaging after successful verification
```

The patch commands stage the changes in each workspace repository. No local
commit or access to the original author's forks is needed.

## Build and verify

Continue in the same Bash session:

```bash
cd "$workspace"
set -o pipefail
./build-hi.sh 2>&1 | tee logs/build.log
(cd artifacts && sha256sum -c SHA256SUMS)
```

The root script builds the Scala distribution with `baseVersionSuffix=bin-hi`,
runs compiler smoke tests, builds and tests Scalariform using its dedicated
`hi-build/` project, runs formatter/compiler integration checks, and packages
the release. The original upstream Scalariform root build is not used because
its old publishing plugins could not be resolved from Maven Central.

Verification includes:

- Batch compilation and execution, constructor fields and mixed English/Hindi.
- Conditional branches, nested and chained conditionals, and evaluation of only
  the selected branch.
- Longer identifiers, backquoted keywords, comments, strings and interpolation.
- Rejection of reassignment to a Hindi `मान`.
- Hindi declarations and conditionals in `IMain` and the presentation compiler.
- Scalariform's library tests, including token offsets, keyword preservation,
  conditional forms and formatting idempotence.
- Formatting the compiler smoke test with the built formatter, then compiling
  and executing that formatted source with the built Hindi compiler.

This recipe was verified on 2026-11-25 with AdoptOpenJDK `1.8.0_265`: the
preparation commands fetched both public upstream baselines into a fresh
workspace, the patched source trees matched the exported source revisions,
and the complete build passed all compiler and integration smoke tests. Scalariform
passed 1,021 tests across 40 suites, with four upstream tests pending. Packaging
produced the six expected files and all four jar checksums verified. A subsequent
documentation review made the component notes portable; only `BUILD-HI.md`
differs from each verified source revision, and the updated patches and tree IDs
were checked again against clean baselines.

This workflow does not run Scala's entire upstream compiler suite. Rebuilt jars
may differ byte for byte from earlier assets because Git metadata and archive
timestamps can differ.

To rerun individual checks after building:

```bash
(cd "$workspace/scala" && ./verify-hi.sh)
(cd "$workspace/scalariform/hi-build" && ../../tools/sbt test)
(cd "$workspace/scalariform" && ./verify-hi.sh)
```

Each patched checkout also contains `BUILD-HI.md` with component details.

## Package and publish release assets

Successful packaging produces exactly:

```text
artifacts/scala-library.jar
artifacts/scala-reflect.jar
artifacts/scala-compiler.jar
artifacts/scalariform.jar
artifacts/SHA256SUMS
artifacts/LICENSES.zip
```

`SHA256SUMS` covers exactly the four jars. `LICENSES.zip` is collected from the
pinned upstream sources and includes Scala's LICENSE, NOTICE and third-party
license files, and Scalariform's MIT license. Keep the matching Scala jars
together. Scalariform also needs scala-xml `1.2.0` and scala-parser-combinators
`1.1.2`; Kojo already provides these. For verification they are staged outside
the release assets, under `scalariform/hi-build/target/runtime-dependencies/`.

To repackage existing build outputs without recompiling:

```bash
cd "$workspace"
python3 tools/package-release.py
(cd artifacts && sha256sum -c SHA256SUMS)
```

Upload the six files as GitHub Release assets and tag the corresponding
`scala-indic` source revision, using `v2.13.18-hi` for the first such release.
For a later release of the same Scala/language combination, use a new tag
instead of replacing an existing published release. Kojo currently requests
`v2.13.18-hi`; a different tag also needs a corresponding Kojo download URL
change or a `-Dkojo.toolchain.url=<full-release-asset-base>` override. Keep
generated workspaces, caches and binaries out of Git. See the `scala-indic`
repository README for attribution and license notices.
