from pathlib import Path
from typing import TYPE_CHECKING

from cheartpy.mesh import import_cheart_mesh
from cheartpy.mesh_tools.interpolation import export_quad_var_from_lin, make_l2qmap
from cheartpy.paraview.api import cheart2vtu_find
from cheartpy.search.api import get_var_index
from pytools.logging import get_logger
from pytools.parallel import ThreadedRunner
from pytools.path import expand_as_path
from pytools.progress import ProgressBar

from data.problems import PILOT_PROBLEMS

if TYPE_CHECKING:
    from cheartpy.paraview.types import APIKwargsFind
    from code_pkg.components import ProblemDef


def interpolate_vars(prob: ProblemDef, n: int = 1) -> None:
    output_dir = prob.get("output_dir", Path.cwd())
    lin_mesh = import_cheart_mesh(
        prob["mesh"]["home"] / prob["mesh"]["top"]["Pres"]["prefix"]
    ).unwrap()
    quad_mesh = import_cheart_mesh(
        prob["mesh"]["home"] / prob["mesh"]["top"]["Disp"]["prefix"]
    ).unwrap()

    l2q_map = make_l2qmap(lin_mesh, quad_mesh)
    var_list = {"P": "Pres"}
    files = expand_as_path([output_dir / f"{p}-*.D" for p in var_list])
    index = get_var_index([f.name for f in files], "P").unwrap()
    var_files = {
        output_dir / f"{k}-{i}.D": output_dir / f"{v}-{i}.D"
        for k, v in var_list.items()
        for i in index
    }
    n_files = len(var_files)
    bart = ProgressBar(n_files)
    log = get_logger()
    log.info(f"Interpolation variables for {output_dir}")
    with ThreadedRunner(thread=n, prog_bar=bart) as executor:
        for lin_file, quad_file in var_files.items():
            executor.submit(export_quad_var_from_lin, l2q_map, lin_file, quad_file, overwrite=True)


def main(prob: ProblemDef, n: int = 1) -> None:
    output_dir = prob.get("output_dir", Path.cwd())
    interpolate_vars(prob, n)
    mesh = prob["mesh"]
    export_vars = ["U", "Pres"]
    kwargs: APIKwargsFind = {
        "mesh": mesh["home"] / mesh["top"]["Disp"]["prefix"],
        "input_dir": output_dir,
        "output_dir": output_dir,
        "var": export_vars,
        "thread": n,
    }
    if prob.get("mode") == "inverse":
        kwargs["space"] = output_dir / "Xi-0.D"
    cheart2vtu_find(**kwargs)


if __name__ == "__main__":
    for p in [p for p_set in PILOT_PROBLEMS.values() for p in p_set]:
        main(p, n=8)
