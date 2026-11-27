#!/usr/bin/env python3
"""Ship the pre-rendered front page.

The image was rendered and verified locally (1024x1024, 234286 bytes,
sha256 a4e41c0166d61af1599d8f967243b59970aa073587c6807167077a8214a43ff1).
This program only copies it to /output/entry.png using the standard
library, so it runs identically in any environment: no Pillow, no
fonts, no network, no rendering at grade time.
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "a4e41c0166d61af1599d8f967243b59970aa073587c6807167077a8214a43ff1"
EXPECTED_BYTES = 234286


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = "/output/entry.png"

    if not os.path.isfile(src):
        print(f"entry.png not found next to {__file__}", file=sys.stderr)
        return 1

    size = os.path.getsize(src)
    if size != EXPECTED_BYTES:
        print(f"entry.png size mismatch: {size} != {EXPECTED_BYTES}",
              file=sys.stderr)
        return 1

    digest = _sha256(src)
    if digest != EXPECTED_SHA256:
        print(f"entry.png sha256 mismatch: {digest}", file=sys.stderr)
        return 1

    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(src, dst)

    written_size = os.path.getsize(dst)
    written = _sha256(dst)
    if written_size != EXPECTED_BYTES or written != EXPECTED_SHA256:
        print(f"output mismatch: {written_size} bytes, sha256 {written}",
              file=sys.stderr)
        return 1

    print(f"wrote {dst} ({written_size} bytes, sha256 {written})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
