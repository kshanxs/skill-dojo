#!/usr/bin/env python3
"""Save a dated copy of a file before it is edited. Never changes the original.

Copies go to `.calligraph/snapshots/` next to the file unless --dir is given.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import shutil
import sys
from pathlib import Path
from typing import List, Optional


def take(path: Path, directory: Optional[Path] = None) -> Path:
    directory = directory or path.parent / ".calligraph" / "snapshots"
    directory.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:10]
    for existing in sorted(directory.glob(f"{path.stem}.*.{digest}{path.suffix}")):
        return existing  # identical content is already saved
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    target = directory / f"{path.stem}.{stamp}.{digest}{path.suffix}"
    shutil.copy2(path, target)
    if hashlib.sha256(target.read_bytes()).hexdigest()[:10] != digest:
        target.unlink()
        raise OSError("the snapshot did not match the original")
    return target


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("file", type=Path)
    parser.add_argument("--dir", type=Path, help="where to store snapshots")
    args = parser.parse_args(argv)
    if not args.file.is_file():
        parser.error(f"no such file: {args.file}")
    print(take(args.file, args.dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
