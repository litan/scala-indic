#!/usr/bin/env python3
"""Stage only the six files needed for a scala-indic release."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import zipfile


def main():
    root = Path(__file__).resolve().parent.parent
    artifacts = root / "artifacts"
    scala_lib = root / "scala/build/pack/lib"
    jars = {
        "scala-library.jar": scala_lib / "scala-library.jar",
        "scala-reflect.jar": scala_lib / "scala-reflect.jar",
        "scala-compiler.jar": scala_lib / "scala-compiler.jar",
        "scalariform.jar": root / "scalariform/hi-build/target/scala-2.13/scalariform.jar",
    }
    expected = set(jars) | {"SHA256SUMS", "LICENSES.zip"}
    artifacts.mkdir(exist_ok=True)
    unexpected = {p.name for p in artifacts.iterdir()} - expected
    if unexpected:
        raise SystemExit("Move unrelated files out of artifacts/ before packaging: " +
                         ", ".join(sorted(unexpected)))

    licenses = {
        "licenses/scala/LICENSE": root / "scala/LICENSE",
        "licenses/scala/NOTICE": root / "scala/NOTICE",
        "licenses/scala/doc/LICENSE.md": root / "scala/doc/LICENSE.md",
        "licenses/scalariform/LICENCE": root / "scalariform/LICENCE",
    }
    for source in sorted((root / "scala/doc/licenses").iterdir()):
        if source.is_file():
            licenses["licenses/scala/doc/licenses/" + source.name] = source
    for source in list(jars.values()) + list(licenses.values()):
        if not source.is_file():
            raise SystemExit("Missing build output or license: " + str(source))

    # Prepare a complete set before replacing any existing release files.
    with tempfile.TemporaryDirectory(prefix=".release-staging-", dir=root) as temporary:
        staged = Path(temporary)
        for name, source in jars.items():
            shutil.copyfile(source, staged / name)
        with zipfile.ZipFile(staged / "LICENSES.zip", "w", zipfile.ZIP_DEFLATED) as archive:
            for name, source in sorted(licenses.items()):
                archive.write(source, name)
        subprocess.run([str(root / "tools/update-checksums.sh"), str(staged)], check=True)
        for name in sorted(expected):
            os.replace(staged / name, artifacts / name)
    print("Release artifacts staged in " + str(artifacts))
    for name in sorted(expected):
        print("  " + name)


if __name__ == "__main__":
    main()
