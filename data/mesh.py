# /// script
# dependencies = []
# ///

from pathlib import Path

from code_pkg.mesh import MeshDef

DEFAULT_CYLINDER: MeshDef = {
    "geo": {
        "shape": (1.0, 0.2, 0.2),
        "size": (20, 10, 10),
        "offset": 0.0,
        "orientation": "x",
        "warp": True,
    },
    "home": Path("mesh") / "cylinder",
    "elem": "HEX",
    "order": 2,
    "top": {"disp": "cyl_quad", "pres": "cyl_lin"},
    "bnds": {"inlet": "inlet", "outlet": "outlet", "inner": "inner", "outer": "outer"},
    "fields": {
        "cl": "CenterLine-0.D",
        "center": "CenterPoint-0.D",
        "fiber": "Fiber-0.D",
        "normal": "Normal-0.D",
    },
}
