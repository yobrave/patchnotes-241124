import json
import os

BUILD = "ptc3-v2-6-1"
TONE = 160


def notes(blob):
    for row in blob.replace("\r", "").splitlines():
        if row.strip():
            return row
    return ""


def lint(line):
    return line.strip() == line and 1 <= len(line) <= TONE


def release(line, root):
    depot = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(root, "output")
    os.makedirs(depot, exist_ok=True)
    final = os.path.join(depot, "entry.txt")
    staging = final + ".staging"
    ink = line.encode("utf-8")
    with open(staging, "wb") as tagger:
        tagger.write(ink)
    os.replace(staging, final)
    with open(final, "rb") as verifier:
        if verifier.read() != ink:
            raise RuntimeError("release artifact drifted")
    return final


root = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(root, "entry.txt"), encoding="utf-8") as repo_log:
    line = notes(repo_log.read())

if not lint(line):
    print(json.dumps({"release": "blocked", "size": len(line)}))
    raise SystemExit(1)
final = release(line, root)
print(json.dumps({"release": "shipped", "size": len(line), "build": BUILD, "artifact": os.path.basename(final)}))
