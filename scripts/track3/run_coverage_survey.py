#!/usr/bin/env python3
"""Run the Track 3 coverage survey end-to-end with one command."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOMS = [
    "living_room",
    "kitchen",
    "bedroom",
    "bathroom",
    "dining_room",
    "hallway",
    "office",
]

REAL_ROOMS = {
    "living_room",
    "kitchen",
    "bedroom",
    "bathroom",
    "dining_room",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-default", type=int, default=0)
    parser.add_argument("--seed-random", type=int, default=17)
    parser.add_argument(
        "--out-dir",
        default=str(Path.home() / "infinigen_out" / "coverage"),
        help="Directory for GLBs, metadata, entity summaries, and combined report",
    )
    parser.add_argument(
        "--summary-name",
        default="coverage_survey_results.json",
        help="Filename for combined summary JSON inside --out-dir",
    )
    args = parser.parse_args()

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    track3_dir = Path(__file__).resolve().parent
    wrapper = track3_dir / "infinigen_wrapper.py"
    extractor = track3_dir / "extract_glb_entities.py"

    runs = []
    for label, seed in (("default", args.seed_default), ("seeded", args.seed_random)):
        for room in ROOMS:
            stem = f"{room}_{label}" if label == "default" else f"{room}_seed{seed}"
            glb_path = out_dir / f"{stem}.glb"
            cmd = [
                sys.executable,
                str(wrapper),
                "--room",
                room,
                "--params-default",
                "--seed",
                str(seed),
                "--out",
                str(glb_path),
                "--quick",
            ]
            print(f"\n==> Running {room} ({label}, seed={seed})")
            result = subprocess.run(cmd, text=True)
            run_info = {
                "room": room,
                "label": label,
                "seed": seed,
                "glb_path": str(glb_path),
                "meta_path": str(glb_path.with_suffix(glb_path.suffix + ".meta.json")),
                "wrapper_exit_code": result.returncode,
            }
            if glb_path.with_suffix(glb_path.suffix + ".meta.json").exists():
                run_info["meta"] = json.loads(
                    glb_path.with_suffix(glb_path.suffix + ".meta.json").read_text()
                )

            if room in REAL_ROOMS and run_info.get("meta", {}).get("output_mode") == "real":
                entities_path = out_dir / f"{stem}.entities.json"
                extract_cmd = [
                    sys.executable,
                    str(extractor),
                    "--glb",
                    str(glb_path),
                    "--out",
                    str(entities_path),
                ]
                extract_result = subprocess.run(extract_cmd, text=True)
                run_info["entities_path"] = str(entities_path)
                run_info["entities_exit_code"] = extract_result.returncode
                if entities_path.exists():
                    run_info["entities"] = json.loads(entities_path.read_text())

            runs.append(run_info)

    summary = {
        "rooms": ROOMS,
        "real_rooms": sorted(REAL_ROOMS),
        "default_seed": args.seed_default,
        "random_seed": args.seed_random,
        "out_dir": str(out_dir),
        "runs": runs,
    }

    summary_path = out_dir / args.summary_name
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"\nWrote combined summary: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
