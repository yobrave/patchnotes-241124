"""Patch notes for the human build, versioned and shipped."""
import os

CHANGELOG = ("v42.0.3: Patched the 3 AM bug where the brain replays "
             "every awkward moment since 2009. Partially effective — "
             "replays now stream in HD.")
BUILD = "ptc2"
CHANNEL = "nightly"
KNOWN = "1 (humans)"


def ship(base):
    base = base or "output"
    os.makedirs(base, exist_ok=True)
    p = os.path.join(base, "entry.txt")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(CHANGELOG + "\n")
    with open(p, "rb") as f:
        blob = f.read()
    return blob.decode("utf-8").strip(), len(blob)


note, size = ship(os.environ.get("MAKEFUN_OUTPUT_DIR"))
if note != CHANGELOG:
    raise SystemExit("rollback initiated")
print(BUILD, CHANNEL, size, "bytes shipped")
print("known issues:", KNOWN, "wontfix")
