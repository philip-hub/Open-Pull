"""
Open-Pull crosshead modification for the ATO 500 kg spoke/pancake load cell
(Amazon B08CK7QNDT, ATO part LC-P02-01).

Load cell (ATO drawing, "500kg~7 ton" row):
    OD 105, body height E = 34, total height H = 37 (boss OD 32 protrudes 3 mm),
    8 x 6.5 mm mounting holes on a 88.9 mm PCD, centre thread M16x1.5.

What this script does (all dimensions mm, machine axis at x=12, y=0, z up):
  * Replaces the old 100 mm / 6xM8 load cell with the ATO cell, flat face up
    against the crosshead, boss facing down toward the upper clamp.
  * Rebuilds the two crosshead plates ("upperMemberSupport") with the 8-hole
    M6 pattern, a 120 mm centre disk (was 105) and a 72 mm hub-relief pocket.
    The lower plate is also re-cut for the Tr10x2 brass flange nuts that are
    actually sold on Amazon (ReliaBot / uxcell: 32 mm flange, 16 mm body,
    4 x M3 on a 24 mm PCD) instead of the 42/25 mm nut in the original CAD.
  * Rebuilds the two side spacers for the new outer bolt positions.
  * Re-drills the wooden crosshead beam ("upperMember") for 4 x M6.
  * Raises the whole crosshead (plates, beam, spacers, cell, flange nuts) by DZ
    so an M16x1.5 jam nut fits between the cell boss and the upper clamp; the
    clamps and specimen stay exactly where they were.
  * Deepens the swivel-nut pocket in both clamp side parts ("SpecimenHolder_
    OuterPart" and "(1)") from 6 to 8.5 mm so a standard 8 mm M16x1.5 thin nut
    fits and the clamp can still yaw (self-align) on it.
  * Adds the new hardware (M6x120 SHCS, washers, nyloc nuts, M16x1.5 rods/nuts)
    and models the top lead-screw nuts as the same brass flange nuts.
  * Writes two assemblies: 500 mm lead screws (original frame) and 400 mm lead
    screws (frame top lowered 100 mm, side pillars 680 mm instead of 780 mm).
  * Exports per-part STEP/STL (STL in print orientation).

Run with a Python that has cadquery:
    python generate_ato_mod.py
"""
import math
import os
import sys

import cadquery as cq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stepio import load  # noqa: E402

SRC_STEP = os.path.join(HERE, "..", "OpenPull-assembly.step")
OUT_STEP = os.path.join(HERE, "STEP")
OUT_STL = os.path.join(HERE, "STL")

# ---------------------------------------------------------------- parameters
AX, AY = 12.0, 0.0           # machine axis

# ATO LC-P02-01 500 kg
CELL_OD, CELL_E, CELL_H = 105.0, 34.0, 37.0
CELL_BOSS_D = 32.0
CELL_PCD = 88.9
CELL_HOLE_D = 6.5
CELL_THREAD_D = 16.0         # M16x1.5 (modelled at nominal)
HOLE_ANGLES = [22.5 + 45.0 * k for k in range(8)]   # cable exits at 0 deg (+x), between two holes

# M16x1.5 hardware: one pack of 8 mm thin nuts (AF 24, e.g. Amazon B0H38TFQ55) for all four positions
JAM_NUT_H = 8.0              # locks the rod against the cell boss
SWIVEL_NUT_H = 8.0           # sits in the clamp swivel pocket, clamp yaws on it
POCKET_H_NEW = 8.5           # swivel pocket height after modification (was 6.0)

# Tr10x2 brass flange nut (ReliaBot B07PVJS888 / uxcell B0DPC24RCB)
FN_FLANGE_D, FN_FLANGE_T, FN_BODY_D, FN_LEN = 32.0, 4.0, 16.0, 19.0
FN_PCD, FN_HOLE_D = 24.0, 3.5
FN_BORE_PLATE = 16.5         # locating bore in the printed plate
FN_PILOT_D, FN_PILOT_DEPTH = 2.8, 10.0   # M3 self-tapping screws into the plate from below

M6_CLEAR_PRINT = 6.8         # clearance in printed parts
M6_CLEAR_WOOD = 7.0          # drill size in the wooden beam
DISK_D = 120.0               # crosshead plate centre disk (old: 105)
FILLET_R = 20.0              # same blend radius as the original plates
RELIEF_D, RELIEF_DEPTH = 72.0, 4.0   # hub clearance pocket in lower plate (old: 55 x 4)
CENTRE_HOLE_D = 36.0         # unchanged
PLATE_T = 12.0
SPACER_H = 49.5              # unchanged (beam is 50)
SPACER_W = 14.0

# original z-levels (from OpenPull-assembly.step)
Z_LOWER_PLATE = 215.0775
Z_BEAM = 227.0775
Z_UPPER_PLATE = 277.0775
Z_SPACER = 227.3665
Z_CLAMP_TOP = 180.0775       # upper clamp top face (unchanged)
Z_NUT_POCKET_TOP = 158.0775  # ceiling of the swivel-nut pocket in the upper clamp
Z_NUT_POCKET_BOT = 152.0775  # original pocket floor (6 mm tall)
Z_LOWER_CLAMP_BOT = -80.9225
Z_LOWER_MEMBER_BOT = -160.9225
Z_MIRROR = (Z_CLAMP_TOP + Z_LOWER_CLAMP_BOT) / 2.0   # lower clamp = upper clamp flipped about this plane
Z_SCREW_BOT = 49.0775        # lead screw bottom end
Z_TOP_BEARING_TOP = 499.0775 # top face of the 3200 bearing / mostUpperMember

# crosshead raise: clamp top -> jam nut -> boss -> cell body -> flat face against the lower plate
DZ = Z_CLAMP_TOP + JAM_NUT_H + CELL_H - Z_LOWER_PLATE

R = CELL_PCD / 2.0
BOLTS = [(AX + R * math.cos(math.radians(a)), AY + R * math.sin(math.radians(a))) for a in HOLE_ANGLES]
BEAM_BOLTS = [p for p in BOLTS if abs(p[0] - AX) < 30.0]      # 4 go through the 60 mm beam
SIDE_BOLTS = [p for p in BOLTS if abs(p[0] - AX) >= 30.0]     # 4 go through the spacers
FN_HOLES = [(FN_PCD / 2 * math.cos(math.radians(45 + 90 * k)), FN_PCD / 2 * math.sin(math.radians(45 + 90 * k)))
            for k in range(4)]


# ---------------------------------------------------------------- helpers
def cyl(d, z0, z1, x=AX, y=AY):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(d / 2.0).extrude(z1 - z0)


def hexnut(af, z0, h, x=AX, y=AY, bore=None):
    n = cq.Workplane("XY").workplane(offset=z0).center(x, y).polygon(6, af / math.cos(math.radians(30))).extrude(h)
    if bore:
        n = n.cut(cyl(bore, z0 - 1, z0 + h + 1, x, y))
    return n


def flange_nut(z_flange_face, body_up, y):
    """Tr10x2 brass flange nut; z_flange_face is the flange face the body sticks out of."""
    s = 1 if body_up else -1
    f0, f1 = sorted((z_flange_face, z_flange_face - s * FN_FLANGE_T))
    b0, b1 = sorted((z_flange_face, z_flange_face + s * (FN_LEN - FN_FLANGE_T)))
    n = cyl(FN_FLANGE_D, f0, f1, AX, y).union(cyl(FN_BODY_D, b0, b1, AX, y))
    n = n.cut(cyl(10, min(f0, b0) - 1, max(f1, b1) + 1, AX, y))
    for hx, hy in FN_HOLES:
        n = n.cut(cyl(FN_HOLE_D, f0 - 1, f1 + 1, AX + hx, y + hy))
    return n


def plate_outline(t):
    """60 x 250 arm (x -18..42) + centre disk, concave corners blended with R20."""
    s = cq.Workplane("XY").center(AX, AY).rect(60, 250).extrude(t)
    s = s.union(cq.Workplane("XY").center(AX, AY).circle(DISK_D / 2.0).extrude(t))
    yc = math.sqrt((DISK_D / 2.0) ** 2 - 30.0 ** 2)
    for x in (AX - 30.0, AX + 30.0):
        for y in (yc, -yc):
            s = s.edges(cq.selectors.BoxSelector((x - 0.5, y - 0.5, -1), (x + 0.5, y + 0.5, t + 1))).fillet(FILLET_R)
    return s


# ---------------------------------------------------------------- new parts (built at z=0, then placed)
def lower_plate():
    """Crosshead plate under the beam; the load cell and the flange nuts sit against its underside (z=0)."""
    p = plate_outline(PLATE_T)
    for y in (100, -100):
        p = p.cut(cyl(FN_BORE_PLATE, -1, PLATE_T + 1, AX, y))
        for hx, hy in FN_HOLES:
            p = p.cut(cyl(FN_PILOT_D, -1, FN_PILOT_DEPTH, AX + hx, y + hy))
    p = p.cut(cyl(RELIEF_D, -1, RELIEF_DEPTH)).cut(cyl(CENTRE_HOLE_D, -1, PLATE_T + 1))
    for x, y in BOLTS:
        p = p.cut(cyl(M6_CLEAR_PRINT, -1, PLATE_T + 1, x, y))
    return p


def upper_plate():
    p = plate_outline(PLATE_T)
    for y in (100, -100):
        p = p.cut(cyl(12, -1, PLATE_T + 1, AX, y))
    for x, y in BOLTS:
        p = p.cut(cyl(M6_CLEAR_PRINT, -1, PLATE_T + 1, x, y))
    return p


def spacer():
    """Obround compression spacer, centred on origin; bolt holes on y = +-17.01."""
    yb = abs(SIDE_BOLTS[0][1])
    s = cq.Workplane("XY").slot2D(2 * yb + SPACER_W, SPACER_W, angle=90).extrude(SPACER_H)
    for y in (yb, -yb):
        s = s.cut(cyl(M6_CLEAR_PRINT, -1, SPACER_H + 1, 0, y))
    return s


def beam():
    """Wooden 60x50x250 crosshead beam (was: 2 x 9 mm holes at y=+-43)."""
    b = cq.Workplane("XY").center(AX, AY).rect(60, 250).extrude(50)
    b = b.cut(cyl(30, -1, 6))
    for y in (100, -100):
        b = b.cut(cyl(26, -1, 4, AX, y)).cut(cyl(12, -1, 51, AX, y))
    for x, y in BEAM_BOLTS:
        b = b.cut(cyl(M6_CLEAR_WOOD, -1, 51, x, y))
    return b


def load_cell(z_flat):
    """ATO LC-P02-01 500 kg, flat (mounting) face at z_flat, boss pointing -z."""
    zb = z_flat - CELL_E
    c = cyl(CELL_OD, zb, z_flat).union(cyl(CELL_BOSS_D, z_flat - CELL_H, zb))
    c = c.cut(cyl(CELL_THREAD_D, z_flat - CELL_H - 1, z_flat + 1))
    for x, y in BOLTS:
        c = c.cut(cyl(CELL_HOLE_D, zb - 1, z_flat + 1, x, y))
    zc = z_flat - CELL_E / 2.0
    gland = (cq.Workplane("YZ", origin=(AX + CELL_OD / 2 - 1, 0, 0)).center(AY, zc).circle(6).extrude(22)
             .union(cq.Workplane("YZ", origin=(AX + CELL_OD / 2 + 4, 0, 0)).center(AY, zc).polygon(6, 19).extrude(9))
             .union(cq.Workplane("YZ", origin=(AX + CELL_OD / 2 + 20, 0, 0)).center(AY, zc).circle(2.5).extrude(40)))
    return c.union(gland)


# ---------------------------------------------------------------- assemble
def build(parts, screw_len):
    root = "TensileTestMachine v6/"
    dtop = screw_len - 500.0                       # frame top / drive top shift for shorter screws

    z_lp = Z_LOWER_PLATE + DZ
    z_flat = z_lp                                  # cell flat face against lower plate
    z_boss = z_flat - CELL_H                       # boss face
    z_up_top = Z_UPPER_PLATE + DZ + PLATE_T
    assert abs(z_boss - JAM_NUT_H - Z_CLAMP_TOP) < 1e-6

    new = {
        "crossHead/upperMemberSupport_lower_ATO": lower_plate().translate((0, 0, z_lp)),
        "crossHead/upperMemberSupport_upper_ATO": upper_plate().translate((0, 0, Z_UPPER_PLATE + DZ)),
        "crossHead/upperMember_beam_ATO": beam().translate((0, 0, Z_BEAM + DZ)),
        "crossHead/spacer_ATO_1": spacer().translate((min(p[0] for p in SIDE_BOLTS), AY, Z_SPACER + DZ)),
        "crossHead/spacer_ATO_2": spacer().translate((max(p[0] for p in SIDE_BOLTS), AY, Z_SPACER + DZ)),
        "crossHead/LoadCell_ATO_LC-P02-01_500kg": load_cell(z_flat),
    }
    for i, y in ((1, 100), (2, -100)):
        new[f"drive_{i}/Tr10x2_flange_nut_crosshead"] = flange_nut(z_lp, True, y)
        new[f"drive_{i}/Tr10x2_flange_nut_top_bearing"] = flange_nut(Z_TOP_BEARING_TOP + dtop + FN_LEN - FN_FLANGE_T, False, y)
        new[f"drive_{i}/leadScrew_Tr10x2_{int(screw_len)}mm"] = cyl(10, Z_SCREW_BOT, Z_SCREW_BOT + screw_len, AX, y)

    hw = {}
    for i, (x, y) in enumerate(BOLTS, 1):
        z_head = z_flat - CELL_E                   # worst case: plain holes, head under the cell ring
        hw[f"M6x120_SHCS_{i}"] = cyl(10, z_head - 6, z_head, x, y).union(cyl(6, z_head, z_head + 120, x, y))
        hw[f"M6_washer_{i}"] = cyl(12, z_up_top, z_up_top + 1.6, x, y).cut(cyl(6.4, z_up_top - 1, z_up_top + 3, x, y))
        hw[f"M6_nyloc_{i}"] = hexnut(10, z_up_top + 1.6, 6, x, y, bore=6)
    # upper clamp: M16x1.5 rod screwed through the cell hub, locked with a nut on the boss;
    # the clamp hangs (and can yaw) on a thin nut sitting in its swivel pocket.
    z_cap = Z_NUT_POCKET_TOP - SWIVEL_NUT_H
    up_len = round((z_flat + 1.5) - (z_cap + 0.5))
    hw["M16x1.5_thin_nut_jam_on_cell_boss"] = hexnut(24, Z_CLAMP_TOP, JAM_NUT_H, bore=16)
    hw["M16x1.5_thin_nut_swivel_upper"] = hexnut(24, z_cap, SWIVEL_NUT_H, bore=16)
    hw[f"M16x1.5_rod_upper_{up_len}mm"] = cyl(16, z_cap + 0.5, z_cap + 0.5 + up_len)
    # lower clamp: same parts mirrored; rod goes down through the bottom beam (not modelled originally)
    z_cap_lo = 2 * Z_MIRROR - Z_NUT_POCKET_TOP                     # pocket ceiling, lower clamp
    lo_top = z_cap_lo + SWIVEL_NUT_H - 0.5
    lo_len = round(lo_top - (Z_LOWER_MEMBER_BOT - 3 - JAM_NUT_H - 3))
    hw["M16x1.5_thin_nut_swivel_lower"] = hexnut(24, z_cap_lo, SWIVEL_NUT_H, bore=16)
    hw["M16_washer_lower"] = cyl(30, Z_LOWER_MEMBER_BOT - 3, Z_LOWER_MEMBER_BOT).cut(
        cyl(17, Z_LOWER_MEMBER_BOT - 4, Z_LOWER_MEMBER_BOT + 1))
    hw["M16x1.5_thin_nut_lower"] = hexnut(24, Z_LOWER_MEMBER_BOT - 3 - JAM_NUT_H, JAM_NUT_H, bore=16)
    hw[f"M16x1.5_rod_lower_{lo_len}mm"] = cyl(16, lo_top - lo_len, lo_top)

    removed = {"crossHead:1/loadCell:1", "crossHead:1/M8x120:1", "crossHead:1/upperMemberSupport:1",
               "crossHead:1/upperMemberSupport (1):1", "crossHead:1/upperMember:1",
               "crossHead:1/spacer:1", "crossHead:1/spacer:2"}
    top_group = ("3200 2RS - bearing:1", "trapezoidalNut2:1", "Clutch:1", "stepper:1", "stepperBracket:1")

    # deepen the swivel-nut pocket in the clamp side parts (both clamps use the same printed parts)
    deepen = Z_NUT_POCKET_TOP - POCKET_H_NEW
    pocket_ext = {
        "SpecimenHolder_OuterPart:1": cq.Solid.makeBox(3.0 + 0.01, 15.0, Z_NUT_POCKET_BOT + 0.01 - deepen,
                                                       pnt=cq.Vector(-3.0, -7.5, deepen)),
        "SpecimenHolder_OuterPart (1):1": cq.Solid.makeBox(3.0 + 0.01, 15.0, Z_NUT_POCKET_BOT + 0.01 - deepen,
                                                           pnt=cq.Vector(23.99, -7.5, deepen)),
    }
    mirror_shape = lambda s: s.mirror("XY", (0, 0, Z_MIRROR))
    modified_outer = {}
    kept = {}
    for k, s in parts.items():
        rel = k[len(root):]
        leaf = rel.split("/")[-1]
        if rel in removed or leaf in ("nut_flange:1", "nut:1", "leadScrew:1"):
            continue                                # replaced by the purchased-nut / new-screw models above
        if leaf in top_group:
            # flange nut on the top bearing is 4 mm taller than the original round nut
            s = s.translate(cq.Vector(0, 0, dtop + (FN_LEN - 15.0 if leaf == "trapezoidalNut2:1" else 0)))
        if leaf == "mostUpperMember:1":
            s = s.translate(cq.Vector(0, 0, dtop))
        if leaf.startswith("sidePillars") and dtop:
            bb = s.BoundingBox()
            s = cq.Solid.makeBox(bb.xlen, bb.ylen, bb.zlen + dtop, pnt=cq.Vector(bb.xmin, bb.ymin, bb.zmin))
            leaf_new = leaf.replace(":", f"_{int(bb.zlen + dtop)}mm:")
            rel = rel.replace(leaf, leaf_new)
        if leaf in pocket_ext:
            cutter = pocket_ext[leaf] if rel.startswith("ClampingYaw1:2/") else mirror_shape(pocket_ext[leaf])
            s = s.cut(cutter)
            if rel.startswith("ClampingYaw1:2/"):
                modified_outer[leaf] = s
            rel = rel.replace(leaf, leaf.replace(":1", "_ATO-pocket:1"))
        kept[rel] = s

    WOOD, PRINT, METAL = cq.Color(0.78, 0.62, 0.42), cq.Color(0.82, 0.82, 0.85), cq.Color(0.62, 0.64, 0.67)
    NEWPRINT, CELL, NEWHW = cq.Color(1.0, 0.45, 0.1), cq.Color(0.35, 0.45, 0.6), cq.Color(0.85, 0.7, 0.2)

    def color_for(rel):
        if rel.startswith("frame:1/") or "beam" in rel:
            return WOOD
        if "ATO" in rel:
            return NEWPRINT
        metal = ("bearing", "stepper:", "leadScrew", "nut", "Clutch", "einschlagmutter")
        return METAL if any(m in rel for m in metal) else PRINT

    asm = cq.Assembly(name=f"OpenPull_ATO500kg_{int(screw_len)}mm-screws")
    subs = {}
    for rel, s in kept.items():
        sub, name = rel.split("/", 1) if "/" in rel else ("misc", rel)
        sub = sub.replace(":", "_")
        subs.setdefault(sub, cq.Assembly(name=sub)).add(
            s, name=name.replace(":", "_").replace("/", "_"), color=color_for(rel))
    for rel, wp in new.items():
        sub, name = rel.split("/")
        color = CELL if "LoadCell" in name else (WOOD if "beam" in name else
                                                 (METAL if ("nut" in name or "Screw" in name) else NEWPRINT))
        subs.setdefault(sub, cq.Assembly(name=sub)).add(wp.val(), name=name, color=color)
    subs["hardware_ATO"] = cq.Assembly(name="hardware_ATO")
    for name, wp in hw.items():
        subs["hardware_ATO"].add(wp.val(), name=name, color=NEWHW)
    for a in subs.values():
        asm.add(a)

    suffix = "" if screw_len == 500 else f"_{int(screw_len)}mm-screws"
    asm.save(os.path.join(OUT_STEP, f"OpenPull-assembly_ATO-500kg{suffix}.step"), exportType="STEP")
    print(f"[{int(screw_len)} mm screws] DZ = {DZ:.1f} mm, M16x1.5 rods: upper {up_len} mm, lower {lo_len} mm")
    return modified_outer


def export_singles(modified_outer):
    """Per-part STEP + STL, centred and in print orientation (flat face on the bed, recesses up)."""
    def on_bed(shape):
        bb = shape.BoundingBox()
        return shape.translate(cq.Vector(-(bb.xmin + bb.xmax) / 2, -(bb.ymin + bb.ymax) / 2, -bb.zmin))

    singles = {  # name: (shape, printable)
        "upperMemberSupport_lower_ATO": (lower_plate().val().rotate((0, 0, 0), (1, 0, 0), 180), True),
        "upperMemberSupport_upper_ATO": (upper_plate().val(), True),
        "spacer_ATO_x2": (spacer().val(), True),
        "SpecimenHolder_OuterPart_ATO-pocket_x2": (modified_outer["SpecimenHolder_OuterPart:1"].rotate((0, 0, 0), (0, 1, 0), -90), True),
        "SpecimenHolder_OuterPart(1)_ATO-pocket_x2": (modified_outer["SpecimenHolder_OuterPart (1):1"].rotate((0, 0, 0), (0, 1, 0), 90), True),
        "upperMember_beam_ATO_wood_drilling_reference": (beam().val(), False),
        "LoadCell_ATO_LC-P02-01_500kg": (load_cell(CELL_H).val(), False),
    }
    for name, (shape, printable) in singles.items():
        shape = on_bed(shape)
        cq.exporters.export(shape, os.path.join(OUT_STEP, name + ".step"))
        if printable:
            cq.exporters.export(shape, os.path.join(OUT_STL, name + ".stl"), tolerance=0.02, angularTolerance=0.1)


if __name__ == "__main__":
    os.makedirs(OUT_STEP, exist_ok=True)
    os.makedirs(OUT_STL, exist_ok=True)
    src = load(SRC_STEP)
    outer = build(src, 500.0)
    build(src, 400.0)
    export_singles(outer)
    print(f"bolts: {[(round(x, 2), round(y, 2)) for x, y in BOLTS]}")
