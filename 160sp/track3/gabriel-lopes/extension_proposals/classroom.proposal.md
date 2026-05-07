# Classroom Extension Proposal

## 1. Target room type and closest existing Infinigen entity

Target room type: `classroom`

Closest existing Infinigen entity: `infinigen.entities.Office`

`Office` is the closest baseline because a classroom is a work-oriented interior with desks or tables, chairs, task lighting, visual focus surfaces, and attention demands. The current Infinigen source has office-related semantics and assets such as desks, monitors, lamps, shelves, and office chairs, but it does not directly express classroom-specific spatial organization.

## 2. Gap analysis

An office-like room cannot fully express a classroom because classrooms require a shared instructional focus rather than only individual workstations. A classroom needs controllable seating organization, such as rows, clusters, or auditorium layouts; variable student density; an instructor focal point; board/front visibility; lighting that remains uniform across learning zones; and acoustic treatment that supports speech intelligibility. It also needs controls for attention and distraction management, because clutter, uneven lighting, and poor sightlines affect how clearly occupants can orient to the learning task.

## 3. Proposed new parameters (JSON-Schema format)

All parameters below are marked with `"status": "proposed"` as required by the assignment.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "ka://extension_proposals/classroom.v1",
  "title": "Classroom Extension Parameters",
  "description": "Proposed parameters for adapting an office-like Infinigen room into a classroom.",
  "closest_existing_entity": "infinigen.entities.Office",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "classroom_seating_layout": {
      "type": "string",
      "enum": ["rows", "clusters", "auditorium"],
      "default": "rows",
      "unit": "n/a",
      "status": "proposed",
      "description": "Arrangement of student seating.",
      "citation": "Kaplan & Kaplan (1989); Joye (2007)",
      "rationale": "Seating layout affects spatial legibility, social organization, and visual complexity in the learning environment."
    },
    "student_density": {
      "type": "number",
      "minimum": 0.3,
      "maximum": 1.5,
      "default": 0.8,
      "unit": "seats_per_m2",
      "status": "proposed",
      "description": "Approximate number of student seats per square meter.",
      "citation": "Ulrich (1991); Joye (2007)",
      "rationale": "Density changes crowding, perceived stress, and the amount of visual information occupants must process."
    },
    "instructor_position": {
      "type": "string",
      "enum": ["front_center", "front_left", "front_right"],
      "default": "front_center",
      "unit": "n/a",
      "status": "proposed",
      "description": "Location of the primary instructor focal point.",
      "citation": "Kaplan & Kaplan (1989)",
      "rationale": "A clear instructional focus supports orientation, coherence, and wayfinding within the room."
    },
    "board_visibility": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "default": 0.8,
      "unit": "normalised",
      "status": "proposed",
      "description": "Normalized visibility of the board or presentation wall from student seating.",
      "citation": "Kaplan & Kaplan (1989); Vartanian et al. (2015)",
      "rationale": "Visibility and perceived enclosure influence how clearly occupants can orient attention toward the main task area."
    },
    "acoustic_treatment": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "default": 0.5,
      "unit": "normalised",
      "status": "proposed",
      "description": "Normalized amount of sound-absorbing wall, ceiling, or floor treatment.",
      "citation": "Ulrich (1991); Joye (2007)",
      "rationale": "Interior material choices affect comfort and environmental stress, so classrooms need a high-level acoustic treatment control."
    },
    "lighting_uniformity": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "default": 0.7,
      "unit": "normalised",
      "status": "proposed",
      "description": "Normalized evenness of daylight and artificial lighting across the classroom.",
      "citation": "Münch et al. (2020); Kaplan & Kaplan (1989)",
      "rationale": "Uniform lighting supports visual comfort and alertness while reducing attention costs from uneven illumination."
    }
  },
  "required": [
    "classroom_seating_layout",
    "student_density",
    "instructor_position",
    "board_visibility",
    "acoustic_treatment",
    "lighting_uniformity"
  ]
}
```

## 4. Implementation hooks

- `infinigen_examples/constraints/semantics.py`: add classroom-specific semantics for student seating, instructor/front zone, board or presentation wall, and acoustic-treatment surfaces.
- `infinigen_examples/constraints/home.py`: add classroom placement constraints that arrange desks/chairs in rows, clusters, or auditorium patterns relative to the instructor position and board.
- `infinigen_examples/generate_indoors.py`: expose a classroom room tag or classroom extension path so the solver can request the new typology rather than treating it as a generic office.
- `infinigen/core/tags.py`: add stable tags for classroom seating, board, instructor zone, and learning-surface classes.
- `infinigen/assets/objects/seating/chairs/office_chair.py`: reuse or subclass existing office chair assets for student seating.
- `infinigen/assets/objects/shelves/simple_desk.py`: reuse or subclass desk assets for student desks and instructor desks.
- `infinigen/assets/objects/wall_decorations/`: add or register board-like wall assets for whiteboards, chalkboards, or presentation surfaces.

These parameters are intended to be exposed at the entity level and consumed by the layout solver without modifying low-level asset generation logic.

## 5. Literature backing

The classroom proposal treats spatial layout, visibility, lighting, density, and material treatment as environmental-psychology controls rather than low-level mesh edits. Kaplan and Kaplan (1989) support the importance of coherence, legibility, and attentional restoration; those ideas motivate clear seating organization, instructor position, and board visibility. Vartanian et al. (2015) supports the relevance of spatial enclosure and approach-avoidance responses, which makes sightlines and focal organization defensible classroom controls.

Lighting and material conditions are also psychologically meaningful. Münch et al. (2020) supports daylight and light exposure as relevant to alertness and human functioning, while Ulrich (1991) and Joye (2007) support the broader role of interior design, material qualities, visual complexity, and biophilic or architectural cues in stress and cognitive response. These references justify exposing only high-level classroom parameters that an LLM can change safely without manipulating solver internals or exact asset IDs.
