# Splat Capture Notes

## Capture Summary

- Room type: `living_room`
- Capture device: Samsung Galaxy S24
- Cloud service used: Polycam
- Export used for the Track 3 pipeline: `living_room.ply`
- Student folder scan path: `160sp/track3/gabriel-lopes/scans/living_room.ply`

## Capture Workflow

I captured one real living-room exemplar with Polycam on a Samsung Galaxy S24 by walking through the room and recording a smooth handheld scan. Polycam processed the capture in the cloud, and I exported the result as a `.ply` file for use with the Track 3 scaffold scripts. I also exported a `.glb` for local inspection in Blender, where I manually marked three material regions for the later `regions.json` file: wall, floor, and couch.

## Processing Time And Retries

I did not record an exact wall-clock processing time during the Polycam session, so I cannot claim a precise duration here. I also do not have any failed retry records that I can document confidently from this capture session. For submission accuracy, I am therefore leaving both the exact processing duration and retry count unspecified rather than inventing them after the fact.

## Surface Assessment

- Wall: captured cleanly enough to define a usable plaster region bounding box.
- Floor: captured cleanly enough to define a usable tile region bounding box.
- Couch: captured cleanly enough to define a usable fabric region bounding box.

These three regions were stable enough in Blender to support manual bounding-box placement for Phase 2.5 material extraction. As expected for a phone-based room capture, the scaffold outputs generated from the course scripts are currently placeholder/stub HDRI and PBR assets rather than full real extracted materials. These outputs were generated using the course scaffold scripts, which currently produce placeholder assets rather than full physically accurate HDRI and PBR materials. However, the signal path worked correctly: the scan file validated, the HDRI wrapper wrote `lighting.hdr` plus metadata, and the material wrapper wrote class-keyed packs plus per-pack manifests.

## Deliverable Notes

For this phase, the important committed artifacts are:

- `160sp/track3/gabriel-lopes/scans/living_room.ply`
- `160sp/track3/gabriel-lopes/regions.json`
- `3d_rooms/living_room/lighting.hdr`
- `3d_rooms/living_room/lighting.hdr.meta.json`
- `3d_rooms/_materials_library/plaster/living_room_wall/`
- `3d_rooms/_materials_library/tile/living_room_floor/`
- `3d_rooms/_materials_library/fabric/living_room_couch/`

The scan artifact is a `.ply` export rather than a `.splat` file. The Phase 2.5 instructions explicitly allow downloading either `.splat` or `.ply`, and the provided Track 3 scaffold scripts accept both formats. The pipeline was executed successfully using the `.ply` file.
