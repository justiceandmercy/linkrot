# linkrot

Scan Markdown documentation for broken internal and external links.

## Features

- Recursively scans directories for `.md` / `.markdown` files.
- Detects inline links and images.
- Validates relative file links against the filesystem.
- Validates `http`/`https` links with a `HEAD` request (falls back to `GET` on `405`).
- Skips anchors, `mailto:`, and `tel:` links.
- Reports file, line, URL, and status for every link.
- Exits non-zero when broken links are found, suitable for CI.

## Install

```bash
pip install -e .
```

## Usage

```bash
# Scan a single file
linkrot README.md

# Scan a directory
linkrot docs/

# Skip external (network) checks
linkrot docs/ --no-external

# Custom timeout
linkrot docs/ --timeout 5
```

Example output:

```
README.md:12 OK https://example.com (HTTP 200)
README.md:15 BROKEN ./missing.md (not found)

docs: 3 files, 42 links, 1 broken
```

## License

MIT
