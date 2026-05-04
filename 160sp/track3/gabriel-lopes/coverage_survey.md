# Track 3 Task 1 Coverage Survey

## Purpose

This coverage survey documents the seven built-in Infinigen Indoors room types before assigned-room manifest work. For each room, I identify the main Infinigen entity, the most useful exposed parameters, their units/ranges, and whether they are meaningful environmental-psychology controls or internal generator scaffolding. The parameter information below comes from the course `extract_infinigen_params.py --all --inspect` script using its fallback `KNOWN_SIGNATURES` list.

## Summary Table

| Room Type | Infinigen Entity | Top 3 Most-Exposed Parameters | Units | Range | What They Affect Visually |
|---|---|---|---|---|---|
| living_room | living_room | ceiling_height_m, daylight_intensity, furniture_density | metres, fraction, fraction | 2.0-3.5; 0.0-1.0; 0.0-1.0 | Room volume/openness; daylight level; clutter/furniture amount |
| kitchen | kitchen | ceiling_height_m, lighting_brightness, layout | metres, fraction, categorical | 2.0-3.5; 0.0-1.0; galley/l_shape/u_shape/island | Room volume; brightness; organization of counters and circulation |
| bedroom | bedroom | ceiling_height_m, lighting_warmth, enclosure | metres, fraction, fraction | 2.0-3.2; 0.0-1.0; 0.0-1.0 | Room volume; warm/cool lighting feeling; sense of enclosure/privacy |
| bathroom | bathroom | ceiling_height_m, glass_area_fraction, fixture_count | metres, fraction, count | 2.0-3.0; 0.0-0.6; 1-6 | Room volume; transparency/openness; density of fixtures |
| dining_room | dining_room | ceiling_height_m, table_size, lighting_intimacy | metres, seats, fraction | 2.2-3.5; 2-12; 0.0-1.0 | Room volume; social group size; intimate vs bright dining atmosphere |
| hallway / corridor | hallway | width_m, ceiling_height_m, lighting_frequency | metres, metres, fraction | 1.0-4.0; 2.0-3.5; 0.0-1.0 | Circulation width; vertical openness; rhythm/frequency of lights |
| office | office | ceiling_height_m, task_lighting, visual_complexity | metres, fraction, fraction | 2.4-3.5; 0.0-1.0; 0.0-1.0 | Room volume; work/task illumination; amount of visual clutter/detail |

## Room Observations

### living_room

The living room parameters that seem most useful for environmental-psychology manipulation are `ceiling_height_m`, `daylight_intensity`, `furniture_density`, `wall_warmth_index`, and `biophilia_count`. These map pretty clearly onto perceived openness, daylight exposure, clutter/social density, material warmth, and restorative nature cues. I would avoid exposing internal generator values like random seeds, object IDs, solver settings, or low-level placement constraints to the LLM because those are not meaningful room-level psychological constructs and could make the generator unstable.

### kitchen

For the kitchen, the most useful parameters are `ceiling_height_m`, `lighting_brightness`, `layout`, and possibly `counter_material`. These affect openness, visibility, workflow, and material feel, which are all interpretable at the room-experience level. `cabinet_color_hue` could also matter, but it should probably be constrained carefully because hue by itself is less meaningful than a more research-grounded color warmth or palette variable. Internal asset choices, exact cabinet IDs, or procedural placement details should not be exposed directly to the LLM.

### bedroom

For the bedroom, `ceiling_height_m`, `lighting_warmth`, `enclosure`, `wall_material`, and `color_saturation` are the most useful controls. These relate to comfort, privacy, relaxation, and perceived safety, which fit the idea of environmental cognition better than purely decorative controls. The LLM should not control implementation-level values like mesh settings, random object placement seeds, or exact bed asset IDs, because those are not psychological variables and could break the room generation.

### bathroom

For the bathroom, `ceiling_height_m`, `glass_area_fraction`, `fixture_count`, and `tile_material` look most useful. These affect perceived openness, privacy, material texture, and crowding/fixture density. However, bathroom parameters should be handled carefully because some changes, like too much glass or too many fixtures, could create unrealistic or uncomfortable designs. The LLM should not touch internal plumbing object IDs, solver constraints, or exact hardware placement values.

### dining_room

For the dining room, `ceiling_height_m`, `table_size`, `lighting_intimacy`, and `material_warmth` are strong room-level controls. These map onto social density, atmosphere, comfort, and formality. I think `table_size` is especially useful because it changes the social meaning of the room, not just the visual layout. Internal object placement settings, exact chair models, or collision/solver parameters should stay hidden from the LLM.

### hallway / corridor

For the hallway/corridor, `width_m`, `ceiling_height_m`, and `lighting_frequency` are useful because they directly affect spaciousness, enclosure, wayfinding, and the rhythm of movement through the space. Hallways are less about furniture and more about navigation, compression, and transition. The LLM should not control low-level wall segment IDs, graph layout internals, door solver settings, or random seeds because those are implementation details rather than meaningful environmental variables.

### office

For the office, the best environmental-psychology parameters are `ceiling_height_m`, `task_lighting`, `openness`, `wall_color_hue`, and `visual_complexity`. These affect perceived spaciousness, work visibility, focus, privacy, and cognitive load. Since office is one of my assigned rooms, I would prioritize parameters that connect to productivity and attention, especially lighting, openness, and visual complexity. I would avoid exposing internal desk IDs, exact asset placement seeds, solver constraints, or mesh-level settings to the LLM.