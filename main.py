from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from cheartpy.cmd_tools.cli import run_prep, run_problem
from cheartpy.io.api import chread_d, chwrite_d_utf

from data.pfile import main_pfile
from data.problems import MAIN_PROBLEMS

if TYPE_CHECKING:
    from code_pkg.components import ProblemDef
    from pytools.arrays import A2
_QUAD_ORDER = 2


def normalize_by_row[F: np.floating](vals: A2[F]) -> A2[F]:
    norm = np.sqrt(np.einsum("...i,...i", vals, vals))
    return vals / norm[:, np.newaxis]


def update_deformed_mesh(prob: ProblemDef) -> None:
    if prob["mode"] != "forward":
        return
    mesh = prob["mesh"]
    c = chread_d(mesh["home"] / "C-0.D")
    r = chread_d(mesh["home"] / "R-0.D")
    z = chread_d(mesh["home"] / "Z-0.D")
    u = chread_d(prob["output_dir"] / prob["name"] / "U-200.D")
    x = chread_d(prob["output_dir"] / prob["name"] / "Xi-0.D")
    f = chread_d(prob["output_dir"] / prob["name"] / "DeformationGradient-200.D")
    f = f.reshape((-1, 3, 3))
    new_c = normalize_by_row(np.einsum("ijk,ik->ij", f, c))
    new_r = normalize_by_row(np.einsum("ijk,ik->ij", f, r))
    new_z = normalize_by_row(np.einsum("ijk,ik->ij", f, z))
    new_x = x + u
    chwrite_d_utf(Path() / "mesh_bent_cylinder" / "C-t.D", new_c)
    chwrite_d_utf(Path() / "mesh_bent_cylinder" / "R-t.D", new_r)
    chwrite_d_utf(Path() / "mesh_bent_cylinder" / "Z-t.D", new_z)
    chwrite_d_utf(Path() / "mesh_bent_cylinder" / "X-t.D", new_x)


def run_pfile(prob: ProblemDef) -> None:
    pfile = main_pfile(prob)
    output_dir = prob.get("output_dir") or Path.cwd()
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    file = (output_dir / prob["name"]).with_suffix(".P")
    with file.open("w") as f:
        pfile.write(f)
    if not (prob["mesh"]["home"] / (prob["mesh"]["top"]["Disp"]["prefix"] + "_FE.PART")).exists():
        run_prep(file)
    run_problem(file, log=True, verbosity="PEDANTIC", cores=8)
    update_deformed_mesh(prob)


if __name__ == "__main__":
    for p in [v for prob_set in MAIN_PROBLEMS.values() for v in prob_set]:
        run_pfile(p)
