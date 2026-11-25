"""Real-life patch note compiler."""
import json
import os
from pathlib import Path

FREEZE = 160
RELEASE = "v5.2.1-r24"
source = Path(__file__).resolve().parent / "entry.txt"
changelog = source.read_bytes().decode("utf-8").strip()
parts = {"note": changelog, "span": len(changelog), "shipped": False}
if 1 <= parts["span"] <= FREEZE:
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    target.mkdir(parents=True, exist_ok=True)
    (target / "entry.txt").write_bytes(changelog.encode("utf-8"))
    parts["shipped"] = True
print(json.dumps(parts))
