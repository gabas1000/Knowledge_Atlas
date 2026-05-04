# Manifest Rationale

## Overview

This rationale explains the parameter choices for the living room and office manifests. The goal is to expose only room-level controls that are meaningful for environmental-cognition research and safe for an LLM front-end to modify.

The parameter names and ranges are based on the course `extract_infinigen_params.py --all --inspect` output and the Task 1 worked example. I am treating these as course-schema controls for the Track 3 pipeline, not as independently verified live constructor arguments from every current Infinigen source file. I also avoid exposing internal generator controls such as random seeds, object IDs, mesh settings, exact asset IDs, and solver constraints because those do not represent psychological constructs and could create invalid generator states.

The cited studies support the environmental-psychology constructs behind the parameters. They do not always define the exact numeric ranges used in the JSON Schema. For normalized 0.0 to 1.0 controls, the range should be understood as a safe generator-facing scale.

## Living Room

### ceiling_height_m

The living room uses a range of 2.0 to 3.5 m, with a default of 2.7 m. Ceiling height is included because it changes perceived spaciousness and enclosure. Meyers-Levy and Zhu (2007) motivate ceiling height as a cognitive-processing variable, and Vartanian et al. (2015) connect ceiling height and perceived enclosure to beauty judgments and approach-avoidance decisions. The numerical range comes from the course manifest/extractor range, not from a direct claim that every value in this range was empirically tested.

### daylight_intensity

The living room uses a normalized daylight range from 0.0 to 1.0, with a default of 0.6. This parameter is included because daylight and natural-light access are relevant to restoration, alertness, mood, and comfort. Kaplan and Kaplan (1989) motivate restorative natural environments, and Münch et al. (2020) support daylight as relevant to human health, alertness, sleep, mood, and circadian functioning. The 0.0 to 1.0 scale is a normalized generator-facing control, not a direct lux measurement.

### wall_warmth_index

The living room uses a normalized wall warmth range from 0.0 to 1.0, with a default of 0.5. This parameter controls the perceived warmth of wall colors and materials. Ulrich (1991) supports the broader idea that interior design can influence wellness and stress-related responses. The exact warmth scale is a design abstraction used to keep the LLM from editing low-level material settings directly.

### furniture_density

The living room uses a normalized furniture density range from 0.0 to 1.0, with a default of 0.4. This parameter affects clutter, crowding, and how visually dense the room feels. Joye (2007) supports the psychological relevance of environmental form, natural contents, and complexity. The range is a bounded generator-control range intended to prevent unrealistic overpopulation of the scene.

### biophilia_count

The living room uses an integer range from 0 to 8, with a default of 2. This parameter controls the number of plant or nature-related elements. Kaplan and Kaplan (1989), Ulrich (1991), and Joye (2007) support the relevance of nature-related cues or biophilic design for restoration, wellness, positive affect, and stress recovery. The 0 to 8 range is a practical scene-design range that keeps the LLM from placing an unrealistic number of plants.

## Office

### ceiling_height_m

The office uses a range of 2.4 to 3.5 m, with a default of 2.7 m. Ceiling height is included because it affects perceived openness, enclosure, and cognition. Meyers-Levy and Zhu (2007) motivate ceiling height as a cognitive-processing variable, and Vartanian et al. (2015) connect ceiling height and enclosure to aesthetic judgments and approach-avoidance decisions. This parameter is especially relevant in an office because the space is intended to support attention and work while still feeling comfortable.

### task_lighting

The office uses a normalized range from 0.0 to 1.0, with a default of 0.7. This parameter controls work lighting intensity. Münch et al. (2020) supports the importance of daylight and lighting for human health, alertness, mood, sleep, and circadian functioning. In the manifest, this is a normalized lighting control rather than a measured lux value because the LLM should modify a safe generator-facing parameter.

### openness

The office uses a normalized range from 0.0 to 1.0, with a default of 0.5. This parameter controls how open or enclosed the office feels. Vartanian et al. (2015) directly supports the importance of perceived enclosure for beauty judgments and approach-avoidance decisions. Joye (2007) also supports the broader relevance of prospect, refuge, openness, and environmental structure. This parameter is safer for the LLM than exposing exact wall positions or solver constraints.

### wall_color_hue

The office uses a normalized hue range from 0.0 to 1.0, with a default of 0.4. This parameter controls wall color at a high level. Ulrich (1991) supports the broader importance of interior design for wellness, but this parameter should be interpreted cautiously because the reference does not define this exact hue range. I kept the parameter because it appeared in the course extractor output, but it is the weakest citation match in the office manifest.

### visual_complexity

The office uses a normalized range from 0.0 to 1.0, with a default of 0.3. This parameter controls the amount of visual detail, clutter, and object complexity. Kaplan and Kaplan (1989) support the importance of environmental legibility, coherence, and restorative experience, while Joye (2007) motivates the psychological relevance of architectural form, biophilic design, and complexity. In an office, visual complexity matters because the environment can either support focus or become distracting.

## Ask-Your-AI Check

I asked the AI to evaluate the candidate parameters for the living room and office manifests using the assignment’s criteria. The AI pushed back on two main issues. First, the parameter ranges mostly come from the course extractor and worked example, not directly from empirical manipulation bands in the papers. Second, `wall_color_hue` is weaker than the other office parameters because the available reference list supports interior design and wellness broadly, but not this exact hue scale. I kept it because it appeared in the course extractor output and because the office manifest needed five parameters, but I described it cautiously.

The strongest parameters are `ceiling_height_m`, `daylight_intensity`, `task_lighting`, `openness`, and `biophilia_count`, because their constructs map more directly onto the assigned reference list. The parameters that should not be exposed are internal generator controls such as seeds, exact object IDs, material-node settings, wall-segment IDs, and solver constraints.

## References

Joye, Y. (2007). Architectural lessons from environmental psychology: The case of biophilic architecture. *Review of General Psychology, 11*(4), 305–328. https://doi.org/10.1037/1089-2680.11.4.305

Kaplan, R., & Kaplan, S. (1989). *The experience of nature: A psychological perspective*. Cambridge University Press.

Meyers-Levy, J., & Zhu, R. (2007). The influence of ceiling height: The effect of priming on the type of processing that people use. *Journal of Consumer Research, 34*(2), 174–186. https://doi.org/10.1086/519146

Münch, M., Wirz-Justice, A., Brown, S. A., Kantermann, T., Martiny, K., Stefani, O., Vetter, C., Wright, K. P., Wulff, K., & Skene, D. J. (2020). The role of daylight for humans: Gaps in current knowledge. *Clocks & Sleep, 2*(1), 61–85. https://doi.org/10.3390/clockssleep2010008

Ulrich, R. S. (1991). Effects of interior design on wellness: Theory and recent scientific research. *Journal of Health Care Interior Design, 3*, 97–109.

Vartanian, O., Navarrete, G., Chatterjee, A., Fich, L. B., Leder, H., Modroño, C., Rostrup, N., Skov, M., Corradi, G., & Nadal, M. (2015). Architectural design and the brain: Effects of ceiling height and perceived enclosure on beauty judgments and approach-avoidance decisions. *Journal of Environmental Psychology, 41*, 10–18. https://doi.org/10.1016/j.jenvp.2014.11.006