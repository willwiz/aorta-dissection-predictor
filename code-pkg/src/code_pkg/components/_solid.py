from typing import TYPE_CHECKING, Literal

from cheartpy.fe.api import create_solver_matrix, create_variable
from cheartpy.fe.physics.api import create_solid_mechanics_problem
from cheartpy.fe.physics.l2_projection import L2SolidProjection
from cheartpy.fe.physics.solid_mechanics.matlaws import Matlaw

from ._types import ModelDef, NeoHookeanDef, Variables

if TYPE_CHECKING:
    from collections.abc import Sequence

    from cheartpy.fe.physics.solid_mechanics.solid_problems import SolidProblem
    from cheartpy.fe.trait import IBCPatch, ISolverMatrix

    from ._types import TopologyMap, TopologyType


def create_solid_variables(
    top: TopologyMap[TopologyType], *, pfx: tuple[str, str, str] | None = None, freq: int = 1
) -> Variables:
    x, u, p = pfx or ("X", "U", "P")
    return Variables(
        Xi=create_variable(f"{x}i", top["Disp"], 3, data=top["Disp"].mesh, freq=freq),
        Xt=create_variable(f"{x}t", top["Disp"], 3, data=top["Disp"].mesh, freq=freq),
        U=create_variable(f"{u}", top["Disp"], 3, freq=freq),
        P=create_variable(f"{p}", top["Pres"], 1, freq=freq),
    )


def create_neohookean_matlaw(model: NeoHookeanDef) -> Matlaw:
    return Matlaw("neohookean-compressible", [model["k"]])


def create_matlaw(model: ModelDef) -> Matlaw:
    match model:
        case {"matlaw": "NeoHookean"}:
            return create_neohookean_matlaw(model)


def create_solid_problem(
    models: Sequence[ModelDef],
    v: Variables,
    bcs: Sequence[IBCPatch],
    *,
    mode: Literal["forward", "inverse"] = "forward",
) -> SolidProblem:
    match mode:
        case "forward":
            mp = create_solid_mechanics_problem(f"Solid{v.U}", "QUASI_STATIC", v.Xi, v.U, pres=v.P)
        case "inverse":
            mp = create_solid_mechanics_problem(f"Solid{v.U}", "QUASI_STATIC", v.Xt, v.U, pres=v.P)
            mp.set_flags("Inverse-mechanics")
    matlaws = [create_matlaw(m) for m in models]
    mp.add_matlaw(*matlaws)
    rho = 1.06e-6
    mp.use_option("Density", rho)
    for bc in bcs:
        mp.bc.add_patch(bc)
    if v.U.order == v.P.order:
        mp.stabilize("Nearly-incompressible", 100)
    return mp


def create_stress_calculation(solid: SolidProblem) -> ISolverMatrix:
    v = create_variable("CauchyStress", solid.variables["Space"].get_top(), 9, freq=1)
    mp = L2SolidProjection(
        f"StressCalc{solid}", solid.variables["Space"], v, solid, "cauchy_stress"
    )
    matrix = create_solver_matrix(f"Matrix{mp}", "SOLVER_MUMPS", mp)
    matrix.add_setting("ordering", "parallel")
    matrix.add_setting("SolverMatrixCalculation", "EVALUATE_EVERY_BUILD")
    return matrix


def create_strain_calculation(solid: SolidProblem) -> ISolverMatrix:
    v = create_variable("DeformationGradient", solid.variables["Space"].get_top(), 9, freq=1)
    mp = L2SolidProjection(
        f"StrainCalc{solid}", solid.variables["Space"], v, solid, "deformation_gradient"
    )
    matrix = create_solver_matrix(f"Matrix{mp}", "SOLVER_MUMPS", mp)
    matrix.add_setting("ordering", "parallel")
    matrix.add_setting("SolverMatrixCalculation", "EVALUATE_EVERY_BUILD")
    return matrix
