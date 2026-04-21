# /// script
# dependencies = []
# ///

from pathlib import Path
from typing import TYPE_CHECKING, Literal, get_args

from code_pkg.components import TopologyType

if TYPE_CHECKING:
    from code_pkg.mesh import MeshDef, MeshDefN

DEFAULT_CYLINDER: MeshDef = {
    "geo": {
        "shape": (9.0, 12.0, 200.0),
        "size": (2, 16, 64),
        "orientation": "x",
        "warp": True,
    },
    "home": Path("mesh"),
    "top": {
        "Disp": {"prefix": "cyl_quad", "elem": "hex", "order": 2},
        "Pres": {"prefix": "cyl_lin", "elem": "hex", "order": 1},
    },
    "bnds": {
        "Inlet": {"name": "Inlet", "tag": 1},
        "Outlet": {"name": "Outlet", "tag": 2},
        "Inner": {"name": "Inner", "tag": 3},
        "Outer": {"name": "Outer", "tag": 4},
    },
    "fields": {
        "a_z": "Az-0.D",
        "center": "CenterPoint-0.D",
        "fiber": "Fiber-0.D",
        "normal": "Normal-0.D",
        "Z": "Z-0.D",
        "C": "C-0.D",
        "R": "R-0.D",
    },
}

NEW_CYLINDER: MeshDefN[TopologyType] = {
    "geo": {
        "shape": (9.0, 12.0, 200.0),
        "size": (2, 16, 64),
        "orientation": "x",
        "warp": False,
    },
    "home": Path("mesh"),
    "top": {
        "Disp": {"mesh": Path("mesh") / "cyl_quad", "elem": "hex", "order": 2},
        "Pres": {"mesh": Path("mesh") / "cyl_lin", "elem": "hex", "order": 1},
        "Inlet": {"mesh": Path("mesh") / "cyl_inlet", "master": "Disp", "bnd": 1},
        "Outlet": {"mesh": Path("mesh") / "cyl_outlet", "master": "Disp", "bnd": 2},
        "Inner": {"mesh": Path("mesh") / "cyl_inner", "master": "Disp", "bnd": 3},
        "Outer": {"mesh": Path("mesh") / "cyl_outer", "master": "Disp", "bnd": 4},
    },
    "bnds": {
        "Inlet": {"name": "Inlet", "tag": 1},
        "Outlet": {"name": "Outlet", "tag": 2},
        "Inner": {"name": "Inner", "tag": 3},
        "Outer": {"name": "Outer", "tag": 4},
    },
    "fields": {
        "a_z": "Az-0.D",
        "center": "CenterPoint-0.D",
        "fiber": "Fiber-0.D",
        "normal": "Normal-0.D",
        "Z": "Z-0.D",
        "C": "C-0.D",
        "R": "R-0.D",
    },
}

DEFORMED_CYLINDER: MeshDef = {
    "geo": {
        "shape": (1.0, 2.0, 5.0),
        "size": (3, 16, 50),
        "orientation": "x",
        "warp": True,
    },
    "home": Path("mesh"),
    "top": {
        "Disp": {"prefix": "cyl_quad", "elem": "hex", "order": 2},
        "Pres": {"prefix": "cyl_lin", "elem": "hex", "order": 1},
    },
    "bnds": {
        "Inlet": {"name": "Inlet", "tag": 1},
        "Outlet": {"name": "Outlet", "tag": 2},
        "Inner": {"name": "Inner", "tag": 3},
        "Outer": {"name": "Outer", "tag": 4},
    },
    "fields": {
        "a_z": "Az-0.D",
        "center": "CenterPoint-0.D",
        "fiber": "Fiber-0.D",
        "normal": "Normal-0.D",
        "Z": "Z-t.D",
        "C": "C-t.D",
        "R": "R-t.D",
    },
}

STRAIGHT_CYLINDER: MeshDef = {
    "geo": {
        "shape": (9.0, 12.0, 200.0),
        "size": (2, 16, 64),
        "orientation": "x",
        "warp": False,
    },
    "home": Path("mesh_straight"),
    "top": {
        "Disp": {"prefix": "quad", "elem": "hex", "order": 2},
        "Pres": {"prefix": "lin", "elem": "hex", "order": 1},
    },
    "bnds": {
        "Inlet": {"name": "Inlet", "tag": 1},
        "Outlet": {"name": "Outlet", "tag": 2},
        "Inner": {"name": "Inner", "tag": 3},
        "Outer": {"name": "Outer", "tag": 4},
    },
    "fields": {
        "a_z": "Az-0.D",
        "center": "CenterPoint-0.D",
        "fiber": "Fiber-0.D",
        "normal": "Normal-0.D",
        "Z": "Z-t.D",
        "C": "C-t.D",
        "R": "R-t.D",
    },
}

PILOT_CYLINDER: MeshDef = {
    "geo": {
        "shape": (1.0, 2.0, 5.0),
        "size": (3, 16, 50),
        "orientation": "x",
        "warp": True,
    },
    "home": Path("mesh_bent_cylinder"),
    "top": {
        "Disp": {"prefix": "cyl_quad", "elem": "hex", "order": 2},
        "Pres": {"prefix": "cyl_lin", "elem": "hex", "order": 1},
    },
    "bnds": {
        "Inlet": {"name": "Inlet", "tag": 1},
        "Outlet": {"name": "Outlet", "tag": 2},
        "Inner": {"name": "Inner", "tag": 3},
        "Outer": {"name": "Outer", "tag": 4},
    },
    "fields": {
        "a_z": "Az-0.D",
        "center": "CenterPoint-0.D",
        "fiber": "Fiber-0.D",
        "normal": "Normal-0.D",
        "Z": "Z-0.D",
        "C": "C-0.D",
        "R": "R-0.D",
    },
}

AortaTopologies = Literal[
    "Disp", "Pres", "Inlet", "Outlet", "Inner", "Outer", "Brachial", "Carotid", "Subclavian"
]
MIA_MESH: MeshDefN[TopologyType] = {
    "label": get_args(TopologyType),
    "geo": {"name": "low"},
    "home": Path("mesh_mia"),
    "top": {
        "Disp": {"mesh": Path("mesh_mia") / "model_quad", "elem": "tet", "order": 2},
        "Pres": {"mesh": Path("mesh_mia") / "model", "elem": "tet", "order": 1},
        "Inner": {"mesh": Path("mesh_mia") / "model_inner", "master": "Pres", "bnd": 3},
        "Outer": {"mesh": Path("mesh_mia") / "model_outer", "master": "Pres", "bnd": 1},
        "Inlet": {"mesh": Path("mesh_mia") / "model_inlet", "master": "Pres", "bnd": 2},
        "Outlet": {"mesh": Path("mesh_mia") / "model_outlet", "master": "Pres", "bnd": 4},
        "Brachial": {"mesh": Path("mesh_mia") / "model_brachial", "master": "Pres", "bnd": 7},
        "Carotid": {"mesh": Path("mesh_mia") / "model_carotid", "master": "Pres", "bnd": 6},
        "Subclavian": {"mesh": Path("mesh_mia") / "model_subclavian", "master": "Pres", "bnd": 5},
    },
    "bnds": {
        "Inlet": {"name": "Inlet", "tag": 2},
        "Outlet": {"name": "Outlet", "tag": 4},
        "Inner": {"name": "Inner", "tag": 3},
        "Outer": {"name": "Outer", "tag": 1},
        "Brachial": {"name": "Brachial", "tag": 7},
        "Carotid": {"name": "Carotid", "tag": 6},
        "Subclavian": {"name": "Subclavian", "tag": 5},
    },
    "fields": {
        "a_z": "Az-0.D",
        "center": "CenterPoint-0.D",
        "fiber": "Fiber-0.D",
        "normal": "Normal-0.D",
        "Z": "Z-0.D",
        "C": "C-0.D",
        "R": "R-0.D",
    },
}
