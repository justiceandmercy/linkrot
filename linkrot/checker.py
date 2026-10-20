import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class Result:
    file: str
    line: int
    url: str
    ok: bool
    reason: str


def check_links(links, timeout=10.0, external=True):
    """Check a list of scanned link dicts and return Result objects."""
    results = []
    for item in links:
        url = item["url"]
        if url.startswith("#") or url.startswith("mailto:") or url.startswith("tel:"):
            results.append(Result(item["file"], item["line"], url, True, "skipped"))
            continue
        parsed = urlparse(url)
        if parsed.scheme in ("http", "https"):
            if not external:
                results.append(
                    Result(item["file"], item["line"], url, True, "external skipped")
                )
                continue
            ok, reason = check_http(url, timeout)
        else:
            base = os.path.dirname(os.path.abspath(item["file"]))
            target = url.split("#", 1)[0]
            if not target:
                ok, reason = True, "anchor only"
            else:
                full = os.path.normpath(os.path.join(base, target))
                ok = os.path.exists(full)
                reason = "exists" if ok else "not found"
        results.append(Result(item["file"], item["line"], url, ok, reason))
    return results


def check_http(url, timeout):
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ok = 200 <= resp.status < 400
            return ok, f"HTTP {resp.status}"
    except urllib.error.HTTPError as exc:
        if exc.code == 405:
            try:
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    ok = 200 <= resp.status < 400
                    return ok, f"HTTP {resp.status}"
            except Exception as exc2:  # noqa: BLE001
                return False, str(exc2)
        return False, f"HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)
