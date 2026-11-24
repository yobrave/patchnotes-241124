"""Patch note entry: run the changelog line through the gate guards, then release it."""
import json
import os
import sys

CHANGELOG = "entry.txt"
RELEASE_CAP = 160


def guards():
    return [
        ("terse_line", lambda t: 0 < len(" ".join(t.split())) <= RELEASE_CAP),
        ("readable_bytes", lambda t: 0 < len(t.encode("utf-8")) < RELEASE_CAP * 4),
        ("single_record", lambda t: t.strip().count("\n") == 0),
        ("version_tagged", lambda t: t.lstrip().lower().startswith("v")),
    ]


def release() -> int:
    with open(CHANGELOG, encoding="utf-8") as feed:
        raw = feed.read()
    passed = [name for name, rule in guards() if rule(raw)]
    blocked = [name for name, rule in guards() if not rule(raw)]
    depot = os.environ.get("MAKEFUN_OUTPUT_DIR", "depot")
    os.makedirs(depot, exist_ok=True)
    with open(os.path.join(depot, CHANGELOG), "wb") as feed:
        feed.write(raw.encode("utf-8"))
    print(json.dumps({"patch": "v42.0.3", "passed": passed, "blocked": blocked, "depot": depot}))
    return 0 if not blocked else 1


if __name__ == "__main__":
    sys.exit(release())
