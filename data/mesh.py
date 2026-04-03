# /// script
# dependencies = []
# ///

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from code_pkg.mesh import MeshDef

DEFAULT_CYLINDER: MeshDef = {
    "geo": {
        "shape": (1.0, 2.0, 5.0),
        "size": (3, 16, 50),
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
