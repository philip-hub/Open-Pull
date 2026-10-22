# Open-Pull: what to 3D print and what to route

This covers the version being built: the **ATO 500 kg load cell** mod with **500 mm lead screws**
(see [the mod README](CAD/TestMachine/ATO-500kg-LoadCell-Mod/README.md)). Paths are relative to this folder.

The machine has three kinds of parts:

* **Printed:** clamps, crosshead plates and spacers, motor brackets, bottom bearing holders, two small lead-screw nuts.
* **Routed:** the wooden frame, which is 4 pieces of 60 × 80 mm stock plus a 60 × 50 mm crosshead beam.
* **Bought:** everything else (load cell, motors, lead screws, bearings, brass nuts, couplers, fasteners).

---

## 3D printed parts

Quantities are for one machine. Files under `CAD/TestMachine/IndividualParts/` share the long prefix
`TensileTestMachine v6_TensileTestMachine v6_`. Only that prefix is left out below; use the first file of each part.

### New or changed for the ATO load cell (already in print orientation)

| Part | Qty | File | Size (mm) | Notes |
|---|---|---|---|---|
| Lower crosshead plate | 1 | `CAD/TestMachine/ATO-500kg-LoadCell-Mod/STL/upperMemberSupport_lower_ATO.stl` | 250 × 120 × 12 | The load cell bolts to it. Has the hub-relief pocket, flange-nut bores and M3 pilot holes. Print pockets up, as exported |
| Upper crosshead plate | 1 | `…/STL/upperMemberSupport_upper_ATO.stl` | 250 × 120 × 12 | |
| Crosshead spacer | **2** | `…/STL/spacer_ATO_x2.stl` | 48 × 14 × 49.5 tall | Print standing up, as exported |
| Clamp side part | **2** | `…/STL/SpecimenHolder_OuterPart_ATO-pocket_x2.stl` | 102 × 80 × 12 | Replaces the original. The nut pocket is deeper for the 8 mm M16 thin nut |
| Clamp side part, mirrored | **2** | `…/STL/SpecimenHolder_OuterPart(1)_ATO-pocket_x2.stl` | 102 × 80 × 12 | Replaces the original |

### Original Open-Pull parts (lay flat in the slicer; they are exported in assembly position)

| Part | Qty | File (after the prefix) | Size (mm) | Notes |
|---|---|---|---|---|
| Clamp body (`Part14`) | 2 | `ClampingYaw1_1_Part14_1_Body1_Part14.stl` | 102 × 80 × 24 | Lay on the big 102 × 80 face |
| Clamping plate | 4 | `ClampingYaw1_1_ClampingPlate_1_Body1_ClampingPlate.stl` | 36 × 30 × 18 | Each holds a 608 bearing. Print with the bearing pocket facing up |
| Clamp knob | 4 | `ClampingYaw1_1_Knob_1_Body1_Knob.stl` | 60 × 60 × 8 | 2 per clamp. The unnamed `ClampingYaw1_1_Body1_.stl` is the same knob |
| Bottom bearing holder (`lowerBearing`) | 2 | `drive_1_lowerBearing_1_Body1_lowerBearing.stl` | 63 × 60 × 53 | Holds the 6202 bearing. Keep the Ø35 bore vertical so it prints round. Screws to the pillar |
| Motor bracket (`stepperBracket`) | 2 | `drive_1_stepperBracket_1_Body1_stepperBracket.stl` | 60 × 50 × 34.5 | Fits the 19:1 motors (same gearbox face as the 14:1). Screws to the pillar |
| Bottom lead-screw nut (`trapezoidalNut1`) | 2 | `drive_1_trapezoidalNut1_1_Body1_trapezoidalNut1.stl` | 24 × 21 × 15 | Printed Tr10x2 thread with a Ø15 spigot that sits in the 6202 bearing |
| Top jam nut (`trapezoidalNut2`) | 2 | `drive_1_trapezoidalNut2_1_Body1_trapezoidalNut2.stl` | 24 × 21 × 7 | Printed Tr10x2 thread. Locks the brass nut on the top bearing |

**Don't print** these, even though they're in `IndividualParts/`:
* `Clutch`: you bought aluminum 8 × 10 mm couplers.
* `upperMemberSupport`, `upperMemberSupport (1)`, `spacer`, `SpecimenHolder_OuterPart*`: replaced by the ATO versions above.
* `loadCell`, `M8x120`, `nut`, `nut_flange`, `einschlagmutter_M8`, the bearings, `stepper`, `leadScrew`: these are models of bought parts.
* `frame_*` and `crossHead_1_upperMember`: wood, see below.

**Optional (in `CAD/Tools/` and `CAD/Specimens/`):**
- Tools: specimen alignment tools, distance gauge, filament clamp, compression jig.
- Test specimens: ISO 527-2 1BA, layer adhesion.
- Test hooks.

### Print settings
| Group | Material | Settings |
|---|---|---|
| Load path: clamp bodies and side parts, clamping plates, crosshead plates, spacers, bearing holders, motor brackets | PETG / PCTG (or PLA+) | 0.2 mm layers, 5–6 walls, 5 top/bottom, 40–50 % gyroid |
| Printed nuts (`trapezoidalNut1/2`) | PETG / PCTG | 0.12 mm layers, 100 % infill, thread axis vertical. Test on the lead screw and run it in a few times |
| Knobs | anything | 3 walls, 20 % |

**Filament:** about 1.4 L of solid part volume. At the settings above that's roughly **1.1–1.3 kg of PETG/PCTG**,
so plan on two 1 kg spools.

**Build plate:** the crosshead plates (250 × 120 mm) are the largest parts and fit a 256 mm Bambu bed.

---

## Routed / machined parts (wood)

Step files for CAM are in `CAD/TestMachine/ATO-500kg-LoadCell-Mod/Routed/`. Each part lies flat at the origin, long side
along X. The original design uses 60 × 80 mm construction timber, which isn't a US lumber size. Mill it from 4×4 posts
(3.5" × 3.5") or laminate 2× stock, then plane to size.

The **60 mm** dimension matters most, because the printed brackets and plates are 60 mm wide.

| Part | Qty | Finished size (mm) | Machining | STEP |
|---|---|---|---|---|
| Side pillar | 2 | 780 × 80 × 60 | None. Pilot holes for the bracket screws are drilled at assembly, using the printed brackets as guides | `side_pillar_x2.step` |
| Foot | 2 | 300 × 80 × 60 | None | `foot_x2.step` |
| Bottom beam (`lowerMember`) | 1 | 260 long × 60 deep × 80 tall | 1 × **Ø17 through** the 80 mm height at the centre (130 from each end, 30 from each side). The lower clamp's M16 rod goes through it | `bottom_beam_lowerMember_x1.step` |
| Top beam (`mostUpperMember`) | 1 | 260 × 60 × 80 tall | 2 stepped holes, centred in the 60 mm depth, **±100 mm from the centre** (30 mm from each end). Each is **Ø30 × 14 deep from the top face** (press fit for the 3200 bearing), then **Ø12 through** | `top_beam_mostUpperMember_x1.step` |
| Crosshead beam (`upperMember`) | 1 | 250 × 60 × 50 tall | **Bottom face:** Ø30 × 6 deep pocket at the centre, and Ø26 × 4 deep pockets at ±100 mm. **Through:** Ø12 at ±100 mm (lead screws), plus 4 × **Ø7** at **±17.01 across × ±41.07 along** from the centre (load-cell bolts). Drawing: `…/images/beam_drilling_and_hole_pattern.png` | `crosshead_beam_upperMember_ATO_x1.step` |

Tolerances: route the Ø30 bearing seats about 0.1 mm undersize for a press fit in wood, and the Ø12 / Ø17 holes
about 0.5 mm oversize for clearance.

The crosshead beam is 250 mm long and slides between pillars that are 260 mm apart, so leave its ends square and
clean. The printed lower crosshead plate can also serve as a drilling jig for the 4 Ø7 holes.

### Frame layout (from the CAD)
- **Pillars:** stand on the feet, with their 60 mm-wide faces facing each other, **260 mm apart** (the 80 mm side runs
  along the beams' length direction).
- **Feet:** run front-to-back under each pillar. Each foot sticks out 100 mm on one side and 140 mm on the other.
- **Bottom beam:** sits between the pillars, flush with the pillar bottoms. Its top face is 80 mm up.
- **Top beam:** sits between the pillars. Its **bottom face is 580 mm** and its top face 660 mm above the pillar bottoms.
  The 120 mm of pillar above it carries the motor brackets.
- **Bottom bearing holders and motor brackets:** screw to the inside faces of the pillars, centred on the lead-screw axis.
- **Joints:** the original CAD doesn't specify how the frame is joined. Glue plus two long structural screws
  (≈ 6 × 120 mm) or M8 threaded rod per joint works well. The frame carries the full test load (up to 5 kN) in bending.

### Optional: route the crosshead plates instead of printing them
`…/STEP/upperMemberSupport_lower_ATO.step` and `…/upperMemberSupport_upper_ATO.step` can be cut from 12 mm
aluminum or birch plywood. Profile and holes are through-cuts. The lower plate also needs:
* a Ø72 × 4 mm pocket on the load-cell side
* 4 × Ø2.8 × 10 mm pilot holes per flange nut (tap M3 in aluminum)
