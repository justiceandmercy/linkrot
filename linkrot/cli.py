import argparse
import os
import sys

from .checker import check_links
from .scanner import scan_markdown


def collect_files(paths):
    out = []
    for path in paths:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for name in files:
                    if name.lower().endswith((".md", ".markdown")):
                        out.append(os.path.join(root, name))
        elif os.path.isfile(path):
            out.append(path)
    return sorted(set(out))


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="linkrot", description="Scan Markdown for broken links."
    )
    parser.add_argument("paths", nargs="+", help="files or directories to scan")
    parser.add_argument("--timeout", type=float, default=10.0, help="HTTP timeout seconds")
    parser.add_argument(
        "--external", dest="external", action="store_true", default=True,
        help="check external http(s) links (default)",
    )
    parser.add_argument(
        "--no-external", dest="external", action="store_false",
        help="skip external http(s) links",
    )
    args = parser.parse_args(argv)

    files = collect_files(args.paths)
    all_links = []
    for filepath in files:
        all_links.extend(scan_markdown(filepath))

    results = check_links(all_links, timeout=args.timeout, external=args.external)
    broken = [r for r in results if not r.ok]
    for result in results:
        status = "OK" if result.ok else "BROKEN"
        print(f"{result.file}:{result.line} {status} {result.url} ({result.reason})")

    print(f"\n{len(files)} files, {len(results)} links, {len(broken)} broken")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
