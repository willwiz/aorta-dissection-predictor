# /// script
# dependencies = []
# ///

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from code_pkg.mesh import MeshDef

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
        "cl": "CenterLine-0.D",
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
        "cl": "CenterLine-0.D",
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
        "cl": "CenterLine-0.D",
        "center": "CenterPoint-0.D",
        "fiber": "Fiber-0.D",
        "normal": "Normal-0.D",
        "Z": "Z-0.D",
        "C": "C-0.D",
        "R": "R-0.D",
    },
}
