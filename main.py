# Patch notes for real-life bugs: one-line changelog exporter (r4).
import json
import pathlib

GATE = {"min": 1, "max": 160}
LABEL = "ptc4-patchnote-r4"


def run():
    here = pathlib.Path(".")
    raw = (here / "entry.txt").read_text(encoding="utf-8")
    body = raw.strip()
    low, high = GATE["min"], GATE["max"]
    if not low <= len(body) <= high:
        return {"result": "gate-blocked", "length": len(body)}
    target = here / "out" / "entry.txt"
    target.parent.mkdir(exist_ok=True)
    target.write_text(body + "\n", encoding="utf-8", newline="\n")
    return {"result": "gate-passed", "length": len(body), "label": LABEL, "gate": GATE}


if __name__ == "__main__":
    print(json.dumps(run()))
