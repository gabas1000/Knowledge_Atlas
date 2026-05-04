#!/usr/bin/env python3
"""infinigen_wrapper.py — Track 3 Task 2 central artifact.

Uses the current Infinigen Indoors command path to generate a room scene,
exports it to glTF/GLB, and writes a metadata sidecar next to the output.

Important honesty note:
- Current Infinigen does not expose `infinigen.entities.LivingRoom`-style room
  classes.
- Current room generation flows through `python -m infinigen_examples.generate_indoors`
  with room-tag overrides such as `restrict_solving.restrict_parent_rooms=["LivingRoom"]`.
- Only a subset of room types are documented as direct single-room solves in the
  checked-in Infinigen source. Unsupported room types fall back clearly and are
  labeled as such in `<out>.meta.json`.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


WRAPPER_VERSION = "0.2.0-current-api"

ROOM_SPECS = {
    "living_room": {
        "tag": "LivingRoom",
        "mode": "real",
        "limitations": [
            "Generated through current Infinigen's indoor solver, not via a per-room Python class.",
            "Track 3 manifest parameters are recorded, but only explicit gin overrides are applied live.",
        ],
    },
    "kitchen": {
        "tag": "Kitchen",
        "mode": "real",
        "limitations": [
            "Generated through current Infinigen's indoor solver, not via a per-room Python class.",
            "Track 3 manifest parameters are recorded, but only explicit gin overrides are applied live.",
        ],
    },
    "bedroom": {
        "tag": "Bedroom",
        "mode": "real",
        "limitations": [
            "Generated through current Infinigen's indoor solver, not via a per-room Python class.",
            "Track 3 manifest parameters are recorded, but only explicit gin overrides are applied live.",
        ],
    },
    "bathroom": {
        "tag": "Bathroom",
        "mode": "real",
        "limitations": [
            "Generated through current Infinigen's indoor solver, not via a per-room Python class.",
            "Track 3 manifest parameters are recorded, but only explicit gin overrides are applied live.",
        ],
    },
    "dining_room": {
        "tag": "DiningRoom",
        "mode": "real",
        "limitations": [
            "Generated through current Infinigen's indoor solver, not via a per-room Python class.",
            "Track 3 manifest parameters are recorded, but only explicit gin overrides are applied live.",
        ],
    },
    "hallway": {
        "tag": "Hallway",
        "mode": "experimental",
        "limitations": [
            "Hallway exists as a room semantic in current Infinigen, but it is not one of the documented single-room examples in HelloRoom.md.",
            "The wrapper attempts real generation with a hallway tag restriction, but output quality or solvability may vary.",
        ],
    },
    "office": {
        "tag": "Office",
        "mode": "fallback",
        "limitations": [
            "Current Infinigen source explicitly notes that office room constraints are not yet written in home_furniture_constraints.",
            "This wrapper therefore does not pretend office is a supported real single-room solve under the current API.",
        ],
    },
}


GLTF_EXPORT_PY = r"""
import bpy, sys
out_path = sys.argv[sys.argv.index('--') + 1]
fmt = 'GLB' if out_path.lower().endswith('.glb') else 'GLTF_EMBEDDED'
bpy.ops.export_scene.gltf(
    filepath=out_path,
    export_format=fmt,
    export_image_format='AUTO',
    export_yup=True,
    export_apply=True,
)
print(f"Wrote {out_path}")
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--room", required=True)
    parser.add_argument("--manifest")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--params")
    group.add_argument("--params-default", action="store_true")
    parser.add_argument("--out", required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()

    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.room not in ROOM_SPECS:
        sys.stderr.write(
            f"Unsupported room_type={args.room!r}. Available: {sorted(ROOM_SPECS)}\n"
        )
        return 1

    params = {} if args.params_default else _load_json(Path(args.params))

    if args.manifest:
        manifest_path = Path(args.manifest).resolve()
        validation_error = _validate_manifest(manifest_path, params)
        if validation_error is not None:
            sys.stderr.write(f"Manifest validation failed: {validation_error}\n")
            return 1
    else:
        manifest_path = None

    t0 = time.time()
    meta = {
        "room_type": args.room,
        "scene_seed": args.seed,
        "resolved_params": params,
        "render_time_seconds": None,
        "wrapper_version": WRAPPER_VERSION,
        "used_real_infinigen_generation": False,
        "output_mode": None,
        "command_api_used": None,
        "limitations": list(ROOM_SPECS[args.room]["limitations"]),
        "ignored_params": [],
        "manifest_path": str(manifest_path) if manifest_path else None,
    }

    spec = ROOM_SPECS[args.room]
    if spec["mode"] == "fallback":
        _write_stub_scene(out_path, args.room)
        meta["output_mode"] = "stub"
        meta["command_api_used"] = "fallback_stub"
        meta["render_time_seconds"] = round(time.time() - t0, 2)
        _write_sidecar(out_path, meta)
        print(f"Fallback: wrote stub for unsupported room {args.room} -> {out_path}")
        return 0

    extra_overrides, ignored_params = _extract_override_params(params)
    meta["ignored_params"] = ignored_params

    with tempfile.TemporaryDirectory(prefix=f"track3_{args.room}_") as tmpdir:
        scene_dir = Path(tmpdir) / "scene"
        scene_dir.mkdir(parents=True, exist_ok=True)
        generation = _run_generate_indoors(
            room=args.room,
            out_dir=scene_dir,
            seed=args.seed,
            quick=args.quick,
            extra_overrides=extra_overrides,
        )
        meta["command_api_used"] = generation["command"]
        meta["used_real_infinigen_generation"] = generation["ok"]
        meta["limitations"].extend(generation["limitations"])

        if not generation["ok"]:
            _write_stub_scene(out_path, args.room)
            meta["output_mode"] = "stub_after_generation_failure"
            meta["render_time_seconds"] = round(time.time() - t0, 2)
            _write_sidecar(out_path, meta)
            sys.stderr.write(generation["error"] + "\n")
            return 0

        blend_path = generation["blend_path"]
        export = export_to_gltf(blend_path, out_path)
        meta["render_time_seconds"] = round(time.time() - t0, 2)

        if export["ok"]:
            meta["output_mode"] = "real"
            _write_sidecar(out_path, meta)
            print(f"OK: rendered {args.room} -> {out_path}")
            return 0

        _write_stub_scene(out_path, args.room)
        meta["output_mode"] = "stub_after_export_failure"
        meta["limitations"].append(export["error"])
        _write_sidecar(out_path, meta)
        sys.stderr.write(export["error"] + "\n")
        return 0


def _load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def _validate_manifest(manifest_path: Path, params: dict) -> str | None:
    try:
        from jsonschema import validate
    except ImportError:
        return None
    try:
        with open(manifest_path) as f:
            manifest = json.load(f)
        validate(instance=params, schema=manifest)
        return None
    except Exception as exc:  # pragma: no cover - passthrough error text
        return str(exc)


def _extract_override_params(params: dict) -> tuple[list[str], list[str]]:
    overrides = []
    ignored = []

    for key in ("gin_overrides", "_gin_overrides", "infinigen_overrides"):
        value = params.get(key)
        if value is None:
            continue
        if isinstance(value, list) and all(isinstance(v, str) for v in value):
            overrides.extend(value)
        else:
            ignored.append(key)

    reserved = {"seed", "gin_overrides", "_gin_overrides", "infinigen_overrides"}
    for key in params:
        if key not in reserved:
            ignored.append(key)

    return overrides, sorted(set(ignored))


def _run_generate_indoors(
    room: str, out_dir: Path, seed: int, quick: bool, extra_overrides: list[str]
) -> dict:
    spec = ROOM_SPECS[room]
    configs = ["singleroom.gin"]
    if quick:
        configs.append("fast_solve.gin")

    overrides = [
        "compose_indoors.terrain_enabled=False",
        f'restrict_solving.restrict_parent_rooms=["{spec["tag"]}"]',
        "restrict_solving.solve_max_rooms=1",
    ]
    overrides.extend(extra_overrides)

    cmd = [
        sys.executable,
        "-m",
        "infinigen_examples.generate_indoors",
        "--task",
        "coarse",
        "--output_folder",
        str(out_dir),
        "--seed",
        str(seed),
        "--configs",
        *configs,
        "--overrides",
        *overrides,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=_resolve_infinigen_repo_root(),
    )
    blend_path = out_dir / "scene.blend"
    limitations = []
    if spec["mode"] == "experimental":
        limitations.append("This run used an experimental hallway tag restriction.")

    if result.returncode != 0 or not blend_path.exists():
        stderr = (result.stderr or result.stdout or "").strip()
        if stderr:
            stderr = stderr[-1200:]
        return {
            "ok": False,
            "blend_path": blend_path,
            "command": " ".join(cmd),
            "limitations": limitations,
            "error": f"Real Infinigen generation failed for {room}: {stderr or 'no output captured'}",
        }

    return {
        "ok": True,
        "blend_path": blend_path,
        "command": " ".join(cmd),
        "limitations": limitations,
        "error": "",
    }


def export_to_gltf(scene_blend_path: Path, out_path: Path) -> dict:
    blender_bin = _resolve_blender()
    if blender_bin is None:
        return {
            "ok": False,
            "error": "Blender executable not found. Set TRACK3_BLENDER or install Blender on PATH.",
        }

    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(GLTF_EXPORT_PY)
        export_script = Path(f.name)

    try:
        result = subprocess.run(
            [
                blender_bin,
                "-b",
                str(scene_blend_path),
                "--python",
                str(export_script),
                "--",
                str(out_path),
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )
    except Exception as exc:  # pragma: no cover - subprocess failure passthrough
        export_script.unlink(missing_ok=True)
        return {"ok": False, "error": f"Blender export failed to start: {exc}"}

    export_script.unlink(missing_ok=True)
    if result.returncode != 0 or not out_path.exists():
        stderr = (result.stderr or result.stdout or "").strip()
        if stderr:
            stderr = stderr[-1200:]
        return {
            "ok": False,
            "error": f"Blender export failed for {scene_blend_path.name}: {stderr or 'no output captured'}",
        }
    return {"ok": True, "error": ""}


def _resolve_blender() -> str | None:
    candidates = [
        os.environ.get("TRACK3_BLENDER"),
        "/Applications/Blender.app/Contents/MacOS/Blender",
        shutil.which("blender"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    return None


def _resolve_infinigen_repo_root() -> str:
    try:
        import infinigen
    except ImportError:
        return os.getcwd()
    return str(Path(infinigen.__file__).resolve().parent.parent)


def _write_sidecar(out: Path, meta: dict) -> None:
    sidecar = out.with_suffix(out.suffix + ".meta.json")
    with open(sidecar, "w") as f:
        json.dump(meta, f, indent=2)


def _write_stub_scene(out: Path, room: str) -> None:
    if out.suffix.lower() == ".gltf":
        out.write_text(json.dumps({"asset": {"version": "2.0"}, "extras": {"room": room}}))
        return

    json_chunk = json.dumps({"asset": {"version": "2.0"}, "extras": {"room": room}}).encode(
        "utf-8"
    )
    json_chunk += b" " * ((4 - len(json_chunk) % 4) % 4)
    total_length = 12 + 8 + len(json_chunk)
    header = b"glTF" + (2).to_bytes(4, "little") + total_length.to_bytes(4, "little")
    chunk_header = len(json_chunk).to_bytes(4, "little") + b"JSON"
    out.write_bytes(header + chunk_header + json_chunk)


if __name__ == "__main__":
    sys.exit(main())
