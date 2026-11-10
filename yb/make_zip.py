"""Build the installable Kodi zip of the YB fork, after checking every skin XML file parses.

Usage (from the repo root):  python3 yb/make_zip.py [--check-only] [--out dist]
Writes dist/<addon id>-<version>.zip with everything under one folder named after the add-on id,
which is what Kodi's "Install from zip file" expects. Fork-only files (yb/, .github/, git files)
are left out.
"""

import argparse
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", ".github", "yb", "dist", "tools", "__pycache__"}
EXCLUDE_FILES = {".gitignore", ".gitattributes", "AGENTS.md"}
EXCLUDE_SUFFIXES = {".xcf", ".pyc"}


def check_xml() -> list[str]:
    errors = []
    for path in [ROOT / "addon.xml", *sorted((ROOT / "1080i").glob("*.xml"))]:
        try:
            ET.parse(path)
        except ET.ParseError as err:
            errors.append(f"{path.relative_to(ROOT)}: {err}")
    return errors


def included(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if rel.parts[0] in EXCLUDE_DIRS or rel.name in EXCLUDE_FILES or path.suffix in EXCLUDE_SUFFIXES:
        return False
    return not rel.name.endswith("~")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the YB fork's Kodi zip")
    parser.add_argument("--check-only", action="store_true", help="only check the XML files")
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    args = parser.parse_args()

    errors = check_xml()
    if errors:
        sys.exit("XML errors:\n" + "\n".join(errors))
    print("All skin XML files parse.")
    if args.check_only:
        return

    addon = ET.parse(ROOT / "addon.xml").getroot()
    addon_id, version = addon.get("id"), addon.get("version")
    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / f"{addon_id}-{version}.zip"
    files = [p for p in sorted(ROOT.rglob("*")) if p.is_file() and included(p)]
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, f"{addon_id}/{path.relative_to(ROOT).as_posix()}")
    print(f"{target} ({len(files)} files, {target.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
