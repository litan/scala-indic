# scala-indic

Patches, build instructions and release binaries for Scala toolchains with
Indic-language keywords, including patched Scalariform for code formatting.
These builds support programming in [Kojo](https://github.com/litan/kojo).

This repository holds versioned patches, build instructions, shared build tools,
license notices and release metadata. Built jars belong in GitHub release assets;
full compiler and formatter source trees are fetched from pinned upstream commits
when rebuilding.

These are independently modified builds. They are not official Scala releases
and are not endorsed by the Scala project. Upstream copyright and attribution
remain with their respective owners.

## Languages

The Hindi build adds five keyword aliases. English keywords continue to work.

| Language | Code | Scala keyword | Localized keyword |
| --- | --- | --- | --- |
| Hindi | `hi` | `val` | `मान` |
| Hindi | `hi` | `var` | `चर` |
| Hindi | `hi` | `def` | `परिभाषा` |
| Hindi | `hi` | `if` | `यदि` |
| Hindi | `hi` | `else` | `अन्यथा` |

```scala
मान सीमा = 10
चर गिनती = 0
परिभाषा दोगुना(संख्या: Int) = संख्या * 2
गिनती = यदि (सीमा > 0) दोगुना(सीमा) अन्यथा 0
```

Additional Indic languages can have their own releases and keyword sets.

## Releases and use

Publish each toolchain as a GitHub Release whose tag identifies the matching
recipe revision. The initial Hindi release uses `v2.13.18-hi`, following the
`v<scala-version>-<language-code>` convention expected by Kojo.

Each release should provide these runtime assets:

| Asset | Purpose |
| --- | --- |
| `scala-library.jar` | Matching Scala standard library |
| `scala-reflect.jar` | Matching reflection library with localized keyword names |
| `scala-compiler.jar` | Compiler that recognizes the localized keywords |
| `scalariform.jar` | Formatter that recognizes the same keywords |
| `SHA256SUMS` | SHA-256 checksums for the four jars |
| `LICENSES.zip` | Upstream license and attribution files |

The Hindi recipe packages these six files together. Its `LICENSES.zip` is
collected from the pinned source checkouts and corresponds to this repository's
`licenses/` directory. Keep notices already embedded inside jars intact. A link
to a license alone is not a replacement for supplying the required license copies.

After downloading a release's four jars and its checksum file into one directory:

```sh
sha256sum -c SHA256SUMS
```

Generate the release checksum file from those exact four jars:

```sh
sha256sum scala-library.jar scala-reflect.jar scala-compiler.jar scalariform.jar > SHA256SUMS
```

Use the matching Scala library, reflect and compiler jars together. Scalariform
also requires the runtime modules listed in the release's build instructions;
Kojo already supplies scala-xml and scala-parser-combinators for the initial
Hindi build.

In Kojo builds with Hindi toolchain support, the toolchain directory is relative
to the Kojo installation root:

```text
<kojo-installation>/toolchains/scala-hi/2.13.18/
```

It contains the four runtime jars and `SHA256SUMS`. Select Hindi and fully restart
Kojo to use the Hindi compiler and editor registration. The current Kojo source
already maps Hindi downloads to
`https://github.com/litan/scala-indic/releases/download/v2.13.18-hi/`.
Publishing the six assets at that tag supplies the files it expects; older Kojo
builds need the corresponding Hindi toolchain support.

Rebuild into a separate workspace using the recipe below, and generate release
checksums from the exact jars being uploaded.

## Build provenance

The Hindi toolchain uses Java 8 and these source baselines:

| Component | Upstream source | Baseline | Modified build version |
| --- | --- | --- | --- |
| Scala | [scala/scala](https://github.com/scala/scala) | `v2.13.18`, commit `98f40d00ddcf59a802862d38a9fe79806cde59fa` | `2.13.18-bin-hi` |
| Scalariform | [bulent2k2/scalariform](https://github.com/bulent2k2/scalariform) | commit `8cf96a69d7a87a4b4d31a4061b8eb1ca615fd896`, before the Turkish additions | `0.2.10-hi` |

The [Hindi 2.13.18 build recipe](hindi/2.13.18/README.md) contains complete patches
against these baselines, including all five aliases, tests and component build
scripts. It also provides the shared build tools, their checksums, pinned tool
versions and commands to fetch, patch, build, verify and package the toolchain.
The recipe records the exact local source commits from which its patches were
exported.

Tag the matching recipe revision when publishing a binary release. Future
versions or languages should have their own recipe directories so a release
always identifies the patches and instructions used for its jars.

### Reference implementation and build guidance

The Turkish Scala toolchain in
[bulent2k2/scala-2](https://github.com/bulent2k2/scala-2), by Bulent Basaran, was
the reference for this work. Its
[Scala 2.13.18 Turkish release](https://github.com/bulent2k2/scala-2/releases/tag/v2.13.18-tr)
provided the compiler patch, build guidance, and release-asset layout that we
adapted for Hindi. The related
[Kojo build notes](https://github.com/bulent2k2/kojo/blob/master/scala-tr/README)
and [Scalariform instructions](https://github.com/bulent2k2/scalariform/blob/master/README_bulent2k2)
also informed the local build process.

The Hindi compiler adds names in `StdNames.scala` and maps them to existing
`VAL`, `VAR`, `DEF`, `IF` and `ELSE` tokens in `Scanners.scala`. The Scalariform
change adds the same five aliases in `lexer/Keywords.scala`. The formatter uses
a dedicated library build to avoid obsolete upstream publishing plugins.

Start with the [versioned build instructions](hindi/2.13.18/README.md). Applying
the patches also creates `scala/BUILD-HI.md` and `scalariform/BUILD-HI.md` in
the rebuild workspace for component-specific details.

Validation of the five-alias build covered compilation and execution, the Scala
interpreter and presentation compiler, rejection of reassignment to `मान`,
conditional evaluation, and formatting that preserves Hindi text. Scalariform
passed 1,021 tests, with four upstream tests pending. These build checks do not
constitute a run of Scala's entire upstream compiler suite.

## Licensing and attribution

### Scala

Scala 2.13.18 is licensed under the
[Apache License, Version 2.0](licenses/scala/LICENSE). Preserve its
[NOTICE](licenses/scala/NOTICE), the
[upstream license overview](licenses/scala/doc/LICENSE.md), and applicable
[third-party license texts](licenses/scala/doc/licenses/). These files are copied
from the exact upstream baseline used for the initial build.

For redistribution, follow [Section 4 of Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0):

- Supply a copy of the Apache 2.0 license with the redistributed work.
- Make modified files carry prominent notices stating that they were changed.
- Retain the relevant upstream copyright and attribution notices in any source
  form that is distributed.
- Include the relevant attribution from the upstream NOTICE in a permitted,
  readable form with the redistributed work.
- Preserve the applicable licenses and notices of included third-party software.

Apache 2.0 permits binary distribution without requiring publication of the
complete modified source tree. Providing exact patches and build instructions
is this project's reproducibility practice, separate from that license's
redistribution conditions. Keep modified build identifiers and release notes
clear about the changes; do not represent these artifacts as official Scala
releases or imply upstream endorsement. Apache 2.0 does not grant general rights
to upstream trademarks.

### Scalariform

Scalariform is separately licensed under the
[MIT License](licenses/scalariform/LICENCE). Include its copyright and permission
notice with distributed copies or substantial portions, including binary
releases. The initial locally built `scalariform.jar` does not embed this text,
so the accompanying license copy is necessary for its distribution.

The presence of Scala's Apache license does not replace Scalariform's MIT
license or the licenses of other bundled components. Refresh the license copies
and component provenance when changing the upstream versions.

### Release preparation

Before publishing each modified toolchain, include the applicable license and
notice files, check that changed files are identified as modified, record the
exact changes and build provenance, and generate checksums from the final jars.
A release description summarizes the modifications; it does not replace required
license copies, attribution or changed-file notices.
