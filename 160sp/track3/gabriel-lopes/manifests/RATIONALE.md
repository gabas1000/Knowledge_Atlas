# Manifest Rationale

## Scope

This document explains the parameter choices for my two assigned Track 3 rooms: `living_room` and `office`. The goal is to expose only room-level controls that are interpretable for environmental-psychology research and safe for an LLM front-end to modify.

For `living_room`, the manifest is grounded in a live current-Infinigen generation path using `Semantics.LivingRoom` restrictions in `infinigen_examples.generate_indoors`. For `office`, the manifest is source-informed rather than live-validated, because current Infinigen does not provide a functioning standalone office room generator in the active indoor constraint path. The current source explicitly says only bedroom, living room, kitchen, bathroom, and dining room have written room constraints, with offices still listed as TODO.

I therefore excluded internal generator controls such as random seeds, object IDs, mesh settings, exact asset IDs, and solver constraints. Those settings are implementation details rather than psychological constructs, and exposing them would make the LLM more likely to create invalid or uninterpretable scenes.

## Living Room

### ceiling_height_m

I kept `ceiling_height_m` at `2.0-3.5 m` with a default of `2.7 m`. This is the strongest living-room parameter because it is directly supported by empirical work on ceiling height, enclosure, and cognition. Meyers-Levy and Zhu (2007) motivate ceiling height as a factor in abstract versus concrete processing, and Vartanian et al. (2015) connect ceiling height and perceived enclosure to beauty judgments and approach-avoidance behavior. The numeric range comes from the course scaffold and is intended as a safe room-design range rather than a claim that every value in that interval was directly tested.

### daylight_intensity

I kept `daylight_intensity` at a normalized `0.0-1.0` range with default `0.6`. Daylight is included because natural light and daylight exposure are tied to restoration, alertness, and circadian functioning. Kaplan and Kaplan (1989) motivate the restorative role of natural environments, and Münch et al. (2020) support the importance of daylight for human health and alertness. The range is normalized because the wrapper needs a bounded generator-facing control rather than a direct lux target.

### wall_warmth_index

I kept `wall_warmth_index` at `0.0-1.0` with default `0.5`. This parameter is a high-level design abstraction for warm versus cool material and palette feel. Ulrich (1991) supports the broader claim that interior design affects wellness and stress-related responses, even though the paper does not define this exact normalized warmth scale. I included it because it gives the LLM a psychologically meaningful atmosphere control without exposing low-level material-node editing.

### furniture_density

I kept `furniture_density` at `0.0-1.0` with default `0.4`. This parameter matters because clutter and visual density affect perceived crowding and cognitive load. Joye (2007) supports the relevance of environmental form and complexity, even though the exact normalized density band is a wrapper-facing design choice rather than a directly studied numeric interval. I preferred this abstraction over exposing asset-by-asset counts because it is higher-level and safer.

### biophilia_count

I kept `biophilia_count` at integer `0-8` with default `2`. This parameter is well motivated because indoor greenery and nature-like cues are strongly connected to restoration and stress reduction. Kaplan and Kaplan (1989), Ulrich (1991), and Joye (2007) all support the relevance of nature-related cues. The range is practical rather than empirical: it is wide enough to vary the scene but bounded enough to prevent unrealistic overpopulation.

## Office

### Why office is different

Office is my assigned room, but it is not live-validated the way `living_room` is. Current Infinigen does contain office-related assets and semantics, such as `OfficeChairFactory`, `OfficeShelfItem`, `SimpleDeskFactory`, `MonitorFactory`, and `DeskLampFactory`, but it does not provide a working standalone office room solve in the current indoor constraint path. I therefore treat the office manifest as a source-informed proposal grounded in the course fallback signature plus the office-related objects and desk constraints present in the codebase.

### ceiling_height_m

I kept `ceiling_height_m` at `2.4-3.5 m` with default `2.7 m`. This remains the strongest office parameter because the empirical support is direct and the construct is easy to interpret in a work setting. Meyers-Levy and Zhu (2007) and Vartanian et al. (2015) motivate it in the same way as for the living room: ceiling height changes openness, enclosure, and cognitive framing. The narrower lower bound reflects the office scaffold range already used in the course helper.

### task_lighting

I kept `task_lighting` at normalized `0.0-1.0` with default `0.7`. This is a defensible office parameter because lighting quality and light exposure are central to workplace alertness and comfort. Münch et al. (2020) is the strongest support from the allowed reference list. The exact numeric band is not an empirical lux band; it is a safe normalized control for a front-end.

### openness

I kept `openness` at normalized `0.0-1.0` with default `0.5`. This is a strong conceptual parameter because perceived enclosure and openness are important environmental-psychology constructs. Vartanian et al. (2015) is the strongest empirical support, and Joye (2007) supports the broader architectural relevance of prospect/refuge style variables. I prefer this abstraction over exposing wall geometry or solver constraints, which would not be safe for the LLM.

### biophilia_count

I replaced the weaker `wall_color_hue` idea with integer `biophilia_count` at `0-6` and default `1`. This is a more defensible office parameter because the allowed reference list gives much stronger support for restorative nature cues than for a free normalized hue slider. Kaplan and Kaplan (1989), Ulrich (1991), and Joye (2007) all support the psychological relevance of natural elements and biophilic cues. The bounded count keeps the parameter interpretable and avoids turning the office into an unrealistic greenhouse.

### visual_complexity

I kept `visual_complexity` at normalized `0.0-1.0` with default `0.3`. This parameter is useful because work environments differ in how much visual information they contain, and that difference plausibly affects focus and cognitive load. Kaplan and Kaplan (1989) support the importance of coherence and legibility, while Joye (2007) supports the psychological relevance of architectural form and complexity. Again, the numeric band is a bounded generator control, not a direct psychometric scale.

## Range Logic

The ranges in both manifests come from a hybrid of three constraints:

1. The course scaffold and fallback signatures already define plausible room-level bounds for Track 3.
2. The cited literature motivates the underlying constructs, even when it does not provide exact numeric generator bands.
3. The manifest should expose only safe, bounded, high-level controls rather than fragile low-level implementation details.

That is why physical dimensions use metric room-scale bounds, while lighting, warmth, openness, and complexity use normalized `0.0-1.0` controls. Those normalized ranges are not claimed as empirical manipulation bands; they are wrapper-facing abstraction layers.

## References

Joye, Y. (2007). Architectural lessons from environmental psychology: The case of biophilic architecture. *Review of General Psychology, 11*(4), 305–328. https://doi.org/10.1037/1089-2680.11.4.305

Kaplan, R., & Kaplan, S. (1989). *The experience of nature: A psychological perspective*. Cambridge University Press.

Meyers-Levy, J., & Zhu, R. (2007). The influence of ceiling height: The effect of priming on the type of processing that people use. *Journal of Consumer Research, 34*(2), 174–186. https://doi.org/10.1086/519146

Münch, M., Wirz-Justice, A., Brown, S. A., Kantermann, T., Martiny, K., Stefani, O., Vetter, C., Wright, K. P., Wulff, K., & Skene, D. J. (2020). The role of daylight for humans: Gaps in current knowledge. *Clocks & Sleep, 2*(1), 61–85. https://doi.org/10.3390/clockssleep2010008

Ulrich, R. S. (1991). Effects of interior design on wellness: Theory and recent scientific research. *Journal of Health Care Interior Design, 3*, 97–109.

Vartanian, O., Navarrete, G., Chatterjee, A., Fich, L. B., Leder, H., Modroño, C., Rostrup, N., Skov, M., Corradi, G., & Nadal, M. (2015). Architectural design and the brain: Effects of ceiling height and perceived enclosure on beauty judgments and approach-avoidance decisions. *Journal of Environmental Psychology, 41*, 10–18. https://doi.org/10.1016/j.jenvp.2014.11.006
