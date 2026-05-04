#!/usr/bin/env python3
"""Extract top-level entity names from a GLB exported by the Track 3 wrapper."""

from __future__ import annotations

import argparse
import json
import re
import struct
from collections import Counter
from pathlib import Path


FACTORY_RE = re.compile(r"([A-Za-z0-9_]+Factory)\(")
ROOM_RE = re.compile(r"^([a-z\-]+_\d+/\d+)$")


def load_glb_json(path: Path) -> dict:
    with path.open("rb") as f:
        magic, version, _ = struct.unpack("<4sII", f.read(12))
        if magic != b"glTF" or version != 2:
            raise ValueError(f"{path} is not a GLB v2 file")
        chunk_len, chunk_type = struct.unpack("<I4s", f.read(8))
        if chunk_type != b"JSON":
            raise ValueError(f"{path} does not start with a JSON chunk")
        data = f.read(chunk_len)
    return json.loads(data.decode("utf-8").rstrip(" \t\r\n\0"))


def simplify_name(name: str) -> str | None:
    if name.startswith("infinigen.__version__="):
        return None
    if name.startswith("hoof_parent_temp"):
        return "wildlife_temp"
    match = FACTORY_RE.search(name)
    if match:
        return match.group(1)
    if ROOM_RE.match(name):
        return name.split("_")[0]
    if name.startswith("door"):
        return "door"
    if name.startswith("window"):
        return "window"
    return name


def summarize(path: Path) -> dict:
    obj = load_glb_json(path)
    scene = obj["scenes"][obj["scene"]]
    indices = scene.get("nodes", [])
    raw_names = [obj["nodes"][idx].get("name", f"node_{idx}") for idx in indices]
    simplified = [name for name in (simplify_name(n) for n in raw_names) if name]
    counts = Counter(simplified)

    return {
        "glb_path": str(path.resolve()),
        "top_level_node_count": len(indices),
        "raw_top_level_names": raw_names,
        "entity_counts": dict(sorted(counts.items())),
        "entity_names_sorted_by_frequency": [name for name, _ in counts.most_common()],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glb", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()

    summary = summarize(Path(args.glb).resolve())
    if args.out:
        out = Path(args.out).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, indent=2))
        print(f"Wrote {out}")
    else:
        print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
