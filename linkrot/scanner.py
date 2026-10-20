import re

LINK_RE = re.compile(r"(?<!\!)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")


def scan_markdown(path):
    """Return a list of link dicts found in a Markdown file."""
    results = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            for match in LINK_RE.finditer(line):
                results.append(
                    {
                        "file": path,
                        "line": lineno,
                        "text": match.group(1),
                        "url": match.group(2),
                        "image": False,
                    }
                )
            for match in IMG_RE.finditer(line):
                results.append(
                    {
                        "file": path,
                        "line": lineno,
                        "text": match.group(1),
                        "url": match.group(2),
                        "image": True,
                    }
                )
    return results
