# /// script
# dependencies = []
# ///

from pathlib import Path
from typing import TYPE_CHECKING

from cheartpy.fe.api import (
    create_pfile,
    create_solver_group,
    create_solver_matrix,
    create_solver_subgroup,
)

from .components import (
    ProblemDef,
    create_boundary_conditions,
    create_cylinder_topologies,
    create_solid_problem,
    create_solid_variables,
    create_strain_calculation,
    create_stress_calculation,
    create_time,
)

if TYPE_CHECKING:
    from cheartpy.fe.trait import IPFile


def main_pfile(p: ProblemDef) -> IPFile:
    time = create_time(p["time"])
    tops = create_cylinder_topologies(p["mesh"])
    svars = create_solid_variables(p["mesh"], tops)
    bc_patches, constraints = create_boundary_conditions(
        mesh=p["mesh"], top=tops, svars=svars, bc=p["bc"]
    )
    solid_prob = create_solid_problem(p, svars, bc_patches)
    solid_matrix = create_solver_matrix("MatrixU", "SOLVER_MUMPS", solid_prob, *constraints)
    solid_matrix.add_setting("ordering", "parallel")
    solid_matrix.add_setting("SolverMatrixCalculation", "EVALUATE_EVERY_BUILD")
    stress_matrix = create_stress_calculation(solid_prob)
    strain_matrix = create_strain_calculation(solid_prob)
    sg_solid = create_solver_subgroup("seq_fp_linesearch", solid_matrix)
    post_calcs = [stress_matrix, strain_matrix]
    sg_post_calcs = [create_solver_subgroup("SOLVER_SEQUENTIAL", calc) for calc in post_calcs]
    g = create_solver_group("Main", time)
    g.set_convergence("L2TOL", 1.0e-9)
    g.set_iteration("LINESEARCHITER", 8)
    g.set_iteration("SUBITERATION", 5)
    g.catch_solver_errors("CATCH_NEWTON_LIMIT")
    g.add_solversubgroup(sg_solid, *sg_post_calcs)
    pfile = create_pfile(output_dir=(p.get("output_dir") or Path.cwd()) / p["name"])
    pfile.add_interface(*tops.ifaces)
    pfile.add_solvergroup(g)
    return pfile
