from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from cheartpy.cl.mesh import create_cl_partition, get_cl_ftype
from cheartpy.cl.var import interp_cl_row_var_to_volume
from cheartpy.io import chread_d, chwrite_d_utf
from cheartpy.search import get_var_index

if TYPE_CHECKING:
    from cheartpy.cl.types import CLDef


def interpolate_cl_v(prefix: str, home: Path, cldef: CLDef) -> None:
    files = [f.name for f in home.glob(rf"{prefix}-*.D")]
    index = get_var_index(files, prefix).unwrap()
    part = create_cl_partition(cldef)
    dtype = get_cl_ftype(cldef)
    match cldef["a_z"]:
        case Path() as p, dtype:
            az = chread_d(p, dtype=dtype)[:, 0]
        case az: ...  # fmt: skip
    for i in index:
        v = chread_d(home / f"{prefix}-{i}.D", dtype=dtype)
        res = interp_cl_row_var_to_volume(az, part, v)
        stiffness = 100 * (res[0] + 1.0)
        chwrite_d_utf(home / f"Mu-{i}.D", stiffness)


def interpolate_cl_expr(prefix: str, home: Path, cldef: CLDef) -> None:
    dtype = get_cl_ftype(cldef)
    match cldef["a_z"]:
        case Path() as p, dtype:
            az = chread_d(p, dtype=dtype)[:, 0]
        case az: ...  # fmt: skip
    stiff = 150 - (90 / (1.0 + np.exp(15.0 * (0.55 - az))))
    chwrite_d_utf(home / f"{prefix}-0.D", stiff)


if __name__ == "__main__":
    interpolate_cl_expr(
        "Mu",
        Path("results_aorta_dettach"),
        {
            "home": Path("mesh_aorta"),
            "a_z": chread_d(Path("mesh_aorta") / "Az-0.D")[:, 0],
            "n": 5,
            "prefix": {"prefix": "CL"},
        },
    )
    # interpolate_cl_v(
    #     "KMult",
    #     Path("results_aorta_dilation"),
    #     {
    #         "home": Path("mesh_aorta"),
    #         "a_z": chread_d(Path("mesh_aorta") / "Az-0.D")[:, 0],
    #         "n": 5,
    #         "prefix": {"prefix": "CL"},
    #     },
    # )
