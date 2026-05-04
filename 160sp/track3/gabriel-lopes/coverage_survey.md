# Track 3 Task 1 Coverage Survey

## Purpose

This coverage survey documents the seven Track 3 indoor room labels using the current Infinigen source available in my setup. The original course scaffold assumes room classes such as `infinigen.entities.LivingRoom`, but the installed Infinigen version does not expose that API. Instead, real room generation works through `python -m infinigen_examples.generate_indoors` with room-tag restrictions such as `restrict_solving.restrict_parent_rooms=["LivingRoom"]`. I therefore treated the five room types that generated successfully as live current-Infinigen evidence, and I treated `hallway` and `office` as limitation cases documented through metadata and failure traces rather than pretending they were real generated rooms.

## Method Summary

- Live generation was run with the Track 3 wrapper for two seeds per room where possible.
- Successful real rooms: `living_room` (`0`, `17`), `kitchen` (`0`, `17`), `bedroom` (`0`, `23`), `bathroom` (`0`, `17`), `dining_room` (`0`, `17`).
- `hallway` was attempted live at seeds `0` and `17`, but both runs failed because the standalone hallway restriction produced no solved room set.
- `office` is unsupported in the current indoor constraint path, so both runs correctly produced fallback stubs rather than real scenes.
- Top-level entity hierarchy was extracted from the exported `.glb` files for the successful rooms.
- Parameter names, units, and ranges below come from the course fallback `KNOWN_SIGNATURES` list in `extract_infinigen_params.py`, because current Infinigen does not provide live `infinigen.entities.*` constructor introspection.

## Summary Table

| Room Type | Infinigen Entity | Top 3 Most-Exposed Parameters | Units | Range | What They Affect Visually |
|---|---|---|---|---|---|
| living_room | Current API tag `Semantics.LivingRoom` via `generate_indoors` | `ceiling_height_m`, `daylight_intensity`, `furniture_density` | metres, fraction, fraction | `2.0-3.5`; `0.0-1.0`; `0.0-1.0` | Volume/openness; daylight level; clutter/furniture amount |
| kitchen | Current API tag `Semantics.Kitchen` via `generate_indoors` | `ceiling_height_m`, `lighting_brightness`, `layout` | metres, fraction, categorical | `2.0-3.5`; `0.0-1.0`; `galley/l_shape/u_shape/island` | Volume; brightness; counter/circulation organization |
| bedroom | Current API tag `Semantics.Bedroom` via `generate_indoors` | `ceiling_height_m`, `lighting_warmth`, `enclosure` | metres, fraction, fraction | `2.0-3.2`; `0.0-1.0`; `0.0-1.0` | Volume; warm/cool ambience; privacy/enclosure |
| bathroom | Current API tag `Semantics.Bathroom` via `generate_indoors` | `ceiling_height_m`, `glass_area_fraction`, `fixture_count` | metres, fraction, count | `2.0-3.0`; `0.0-0.6`; `1-6` | Volume; openness/privacy; fixture density |
| dining_room | Current API tag `Semantics.DiningRoom` via `generate_indoors` | `ceiling_height_m`, `table_size`, `lighting_intimacy` | metres, seats, fraction | `2.2-3.5`; `2-12`; `0.0-1.0` | Volume; social group size; intimate vs bright atmosphere |
| hallway | Experimental current API tag `Semantics.Hallway`; live attempt failed | `width_m`, `ceiling_height_m`, `lighting_frequency` | metres, metres, fraction | `1.0-4.0`; `2.0-3.5`; `0.0-1.0` | Circulation width; vertical openness; rhythm of lights |
| office | No working live room generator in current indoor constraint path; fallback only | `ceiling_height_m`, `task_lighting`, `visual_complexity` | metres, fraction, fraction | `2.4-3.5`; `0.0-1.0`; `0.0-1.0` | Volume; task illumination; visual clutter/detail |

## Room Observations

### living_room

Two live runs succeeded at seeds `0` and `17`. Across those runs, the most visible recurring top-level entities were `NatureShelfTrinketsFactory`, `BookStackFactory`, `window`, `CeilingLightFactory`, `DeskLampFactory`, `TVStandFactory`, `SofaFactory`, and storage furniture such as `CellShelfFactory` and `KitchenCabinetFactory`. For environmental-psychology manipulation, `ceiling_height_m`, `daylight_intensity`, `furniture_density`, `wall_warmth_index`, and `biophilia_count` remain the most useful controls because they map onto openness, brightness, clutter, material warmth, and restorative cues. The LLM should not touch internal scaffolding such as exact asset IDs, placeholder vs asset distinctions, wildlife/noise objects, camera rigs, or solver-specific layout internals.

### kitchen

Two live runs succeeded at seeds `0` and `17`. The kitchen hierarchy repeatedly exposed `window`, `CeilingLightFactory`, `WallArtFactory`, `OvenFactory`, `KitchenCabinetFactory`, `KitchenSpaceFactory`, `DishwasherFactory`, `BeverageFridgeFactory`, `FoodBoxFactory`, `CanFactory`, `BottleFactory`, and related pantry/counter objects. For usable environmental controls, `ceiling_height_m`, `lighting_brightness`, `layout`, `counter_material`, and `cabinet_color_hue` are the clearest candidates because they influence openness, visibility, workflow, and material character. The LLM should not directly manipulate low-level kitchen asset factories, exact pantry-object counts, or procedural placement internals because those are implementation details rather than defensible room-level variables.

### bedroom

The default bedroom run succeeded at seed `0`, the first random seed `17` failed due to an internal Infinigen asset bug, and a replacement random run succeeded at seed `23`. Across the successful runs, the strongest recurring bedroom entities were `window`, `NatureShelfTrinketsFactory`, `BookStackFactory`, `BedFactory`, `CeilingLightFactory`, `FloorLampFactory`, `DeskLampFactory`, `SimpleBookcaseFactory`, and some desk/storage furniture. For environmental-psychology use, `ceiling_height_m`, `lighting_warmth`, `enclosure`, `wall_material`, and `color_saturation` are the best high-level controls because they connect to privacy, comfort, relaxation, and affective tone. I would keep the LLM away from generator noise such as exact plant/decor asset identities, wildlife placeholders, and scene-assembly mechanics.

### bathroom

Two live runs succeeded at seeds `0` and `17`. The real bathroom outputs consistently showed `window`, `HardwareFactory`, `BottleFactory`, `StandingSinkFactory`, `ToiletFactory`, `BathtubFactory`, `SingleCabinetFactory`, `CeilingLightFactory`, and mirror/wall-art elements. The most useful exposed controls remain `ceiling_height_m`, `glass_area_fraction`, `fixture_count`, and `tile_material`, because they alter openness, privacy, density, and material feel in interpretable ways. The LLM should not manipulate plumbing-specific asset identities, hardcoded hardware layout, or low-level object-support rules, since those are structural generator details rather than psychologically meaningful room parameters.

### dining_room

Two live runs succeeded at seeds `0` and `17`. The dining-room hierarchy repeatedly included `window`, `ChairFactory`, `TableDiningFactory`, `CeilingLightFactory`, `CupFactory`, `BowlFactory`, `WineglassFactory`, `PlateFactory`, `BookStackFactory`, `NatureShelfTrinketsFactory`, and supporting shelves/cabinets. `ceiling_height_m`, `table_size`, `lighting_intimacy`, and `material_warmth` are the best room-level controls because they directly influence social density, formality, and the emotional tone of shared meals. The LLM should not be allowed to micromanage individual dishware or chair counts at the factory level, because those look more like scene-construction internals than defensible psychology variables.

### hallway

Both hallway runs were attempted live at seeds `0` and `17`, but both failed in current Infinigen because the standalone hallway restriction produced no solved room set. That means I do not have a real hallway hierarchy to report, and I should not pretend otherwise. I can still list `width_m`, `ceiling_height_m`, and `lighting_frequency` as plausible hallway-facing controls from the fallback signature scaffold, because those match the kinds of spatial and navigational properties one would want to manipulate in a corridor. However, this row should be interpreted as a limitation case: source-recognized room tag, attempted live generation, but no validated standalone hallway output in the current version.

### office

Office is my assigned room, but current Infinigen does not provide a working standalone office generator in the active indoor constraint path, so both office runs correctly produced fallback stubs instead of real rooms. Because of that, I do not have a live office hierarchy and cannot honestly claim one. The office parameters here should be treated as a source-informed proposal built from the course fallback signature plus office-related concepts that do exist in the codebase, such as desks, monitors, lamps, shelving, and `OfficeChairFactory`/`OfficeShelfItem` semantics. The most useful controls still appear to be `ceiling_height_m`, `task_lighting`, `openness`, `wall_color_hue`, and `visual_complexity`, but they are not live-validated against a generated office scene in this version.

## Bottom Line

For Phase 2, the strongest defensible subset comes from the five real current-Infinigen room types: `living_room`, `kitchen`, `bedroom`, `bathroom`, and `dining_room`. `hallway` and `office` should remain in the table because the assignment asks for all seven room types, but they must be labeled honestly as limitation cases rather than treated as fully supported live entity hierarchies.
