# /// script
# dependencies = []
# ///

from pathlib import Path
from typing import TYPE_CHECKING, Literal, get_args

from code_pkg.mesh import DissectedType, MeshDef, MeshDefN, TopologyType

if TYPE_CHECKING:
    from cheartpy.fe.aliases import VolumeTopologyDef

TEMPLATE_AORTA: VolumeTopologyDef = {
    "elem": "tet",
    "order": 1,
    "mesh": Path("mesh_aorta") / "model",
}

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
        "a_c": "Ac-0.D",
        "a_r": "Ar-0.D",
        "Z": "Z-0.D",
        "C": "C-0.D",
        "R": "R-0.D",
    },
}

NEW_CYLINDER: MeshDefN[TopologyType] = {
    "geo": {
        "shape": (9.0, 12.0, 1000.0),
        "size": (3, 16, 100),
        "orientation": "x",
        "warp": False,
    },
    "home": Path("mesh"),
    "top": {
        "Disp": {"mesh": Path("mesh") / "quad", "elem": "hex", "order": 2},
        "Pres": {"mesh": Path("mesh") / "lin", "elem": "hex", "order": 1},
        "Inlet": {"mesh": Path("mesh") / "inlet", "master": "Disp", "bnd": 1},
        "Outlet": {"mesh": Path("mesh") / "outlet", "master": "Disp", "bnd": 2},
        "Inner": {"mesh": Path("mesh") / "inner", "master": "Disp", "bnd": 3},
        "Outer": {"mesh": Path("mesh") / "outer", "master": "Disp", "bnd": 4},
    },
    "bnds": {
        "Inlet": {"name": "Inlet", "tag": 1},
        "Outlet": {"name": "Outlet", "tag": 2},
        "Inner": {"name": "Inner", "tag": 3},
        "Outer": {"name": "Outer", "tag": 4},
    },
    "fields": {
        "a_z": "Az-0.D",
        "a_c": "Ac-0.D",
        "a_r": "Ar-0.D",
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
        "a_c": "Ac-0.D",
        "a_r": "Ar-0.D",
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
        "a_c": "Ac-0.D",
        "a_r": "Ar-0.D",
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
        "a_c": "Ac-0.D",
        "a_r": "Ar-0.D",
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
        "a_c": "Ac-0.D",
        "a_r": "Ar-0.D",
        "Z": "Z-0.D",
        "C": "C-0.D",
        "R": "R-0.D",
    },
}

HOME = Path("mesh_plane")
AORTA_MESH: MeshDefN[TopologyType] = {
    "label": get_args(TopologyType),
    "geo": {"name": "full"},
    "home": HOME,
    "top": {
        "Disp": {"mesh": HOME / "Quad", "elem": "tet", "order": 2},
        "Pres": {"mesh": HOME / "Lin", "elem": "tet", "order": 1},
        "Inner": {"mesh": HOME / "Inner", "master": "Pres", "bnd": 3},
        "Outer": {"mesh": HOME / "Outer", "master": "Pres", "bnd": 1},
        "Inlet": {"mesh": HOME / "Inlet", "master": "Pres", "bnd": 2},
        "Outlet": {"mesh": HOME / "Outlet", "master": "Pres", "bnd": 4},
        "Brachial": {"mesh": HOME / "Brachial", "master": "Pres", "bnd": 7},
        "Carotid": {"mesh": HOME / "Carotid", "master": "Pres", "bnd": 6},
        "Subclavian": {"mesh": HOME / "Subclavian", "master": "Pres", "bnd": 5},
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
        "a_c": "Ac-0.D",
        "a_r": "Ar-0.D",
        "Z": "Z-0.D",
        "C": "C-0.D",
        "R": "R-0.D",
    },
}


DISSECTION_MESH: MeshDefN[DissectedType] = {
    "label": get_args(DissectedType),
    "geo": {"name": "full"},
    "home": Path("mesh_aorta"),
    "top": {
        "Disp": {"mesh": Path("mesh_aorta") / "Quad", "elem": "tet", "order": 1},
        "Pres": {"mesh": Path("mesh_aorta") / "Lin", "elem": "tet", "order": 1},
        "Inner": {"mesh": Path("mesh_aorta") / "Inner", "master": "Pres", "bnd": 3},
        "Outer": {"mesh": Path("mesh_aorta") / "Outer", "master": "Pres", "bnd": 7},
        "Inlet": {"mesh": Path("mesh_aorta") / "Inlet", "master": "Pres", "bnd": 15},
        "Outlet": {"mesh": Path("mesh_aorta") / "Outlet", "master": "Pres", "bnd": 2},
        "Brachial": {"mesh": Path("mesh_aorta") / "Brachial", "master": "Pres", "bnd": 3},
        "Carotid": {"mesh": Path("mesh_aorta") / "Carotid", "master": "Pres", "bnd": 4},
        "Subclavian": {"mesh": Path("mesh_aorta") / "Subclavian", "master": "Pres", "bnd": 11},
        "ca1": {"mesh": Path("mesh_aorta") / "ca1", "master": "Pres", "bnd": 1},
        "ca2": {"mesh": Path("mesh_aorta") / "ca2", "master": "Pres", "bnd": 8},
    },
    "bnds": {
        "Inner": {"name": "Inner", "tag": 3},
        "Outer": {"name": "Outer", "tag": 7},
        "Inlet": {"name": "Inlet", "tag": 15},
        "Outlet": {"name": "Outlet", "tag": 2},
        "Brachial": {"name": "Brachial", "tag": 3},
        "Carotid": {"name": "Carotid", "tag": 4},
        "Subclavian": {"name": "Subclavian", "tag": 11},
        "ca1": {"name": "ca1", "tag": 1},
        "ca2": {"name": "ca2", "tag": 8},
    },
    "fields": {
        "a_z": "Az-0.D",
        "a_c": "Ac-0.D",
        "a_r": "Ar-0.D",
        "Z": "Z-0.D",
        "C": "C-0.D",
        "R": "R-0.D",
    },
}
