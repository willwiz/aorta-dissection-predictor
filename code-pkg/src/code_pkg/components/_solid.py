from collections.abc import Mapping
from typing import TYPE_CHECKING

from cheartpy.fe.api import create_expr, create_solver_matrix, create_variable
from cheartpy.fe.physics.api import create_solid_mechanics_problem
from cheartpy.fe.physics.l2_projection import L2SolidProjection
from cheartpy.fe.physics.solid_mechanics.matlaws import Matlaw

from ._types import (
    ModelDef,
    NeoHookeanDef,
    ProblemDef,
    TopologyMap,
    Variables,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from cheartpy.fe.physics.solid_mechanics.solid_problems import ResidualStrainArgs, SolidProblem
    from cheartpy.fe.trait import IBCPatch, ISolverMatrix

    from code_pkg.mesh import MeshDefN, TopologyType


def create_solid_variables(
    prob: ProblemDef,
    top: TopologyMap[TopologyType],
    *,
    pfx: tuple[str, str, str] | None = None,
    freq: int = 1,
) -> Variables:
    x, u, p = pfx or ("X", "U", "P")
    space = prob["mesh"]["home"] / "X-t.D" if (prob.get("mode") == "inverse") else top["Disp"].mesh
    return Variables(
        Xi=create_variable(f"{x}i", top["Disp"], 3, data=space, freq=freq),
        X0=create_variable(f"{x}0", top["Disp"], 3, space, freq=freq),
        U=create_variable(f"{u}", top["Disp"], 3, freq=freq),
        P=create_variable(f"{p}", top["Pres"], 1, freq=freq),
    )


def create_neohookean_matlaw(model: NeoHookeanDef) -> Matlaw:
    return Matlaw("neohookean", [model["k"]])


def create_matlaw(model: ModelDef) -> Matlaw:
    match model:
        case {"matlaw": "NeoHookean"}:
            return create_neohookean_matlaw(model)

def _create_residual_strain_tensor[T](
    mesh: MeshDefN[T], solid: SolidProblem, strain: float
) -> ResidualStrainArgs:
    top = solid.variables["Displacement"].get_top()
    z = create_variable("Z", top, 3, data=mesh["home"] / mesh["fields"]["Z"], freq=1)
    c = create_variable("C", top, 3, data=mesh["home"] / mesh["fields"]["C"], freq=1)
    r = create_variable("R", top, 3, data=mesh["home"] / mesh["fields"]["R"], freq=1)
    longitudinal_stretch = create_expr("axial_stretch", [f"1.0 + {strain}*min(t, 1.0)"])
    offaxis_compression = create_expr(
        "offaxis_compression", [f"1.0 / sqrt({longitudinal_stretch})"]
    )
    res_z = create_expr(
        "residual_z",
        [f"{longitudinal_stretch} * {z}.{i} * {z}.{j}" for i in [1, 2, 3] for j in [1, 2, 3]],
    )
    res_c = create_expr(
        "residual_c",
        [f"{offaxis_compression} * {c}.{i} * {c}.{j}" for i in [1, 2, 3] for j in [1, 2, 3]],
    )
    res_r = create_expr(
        "residual_r",
        [f"{offaxis_compression} * {r}.{i} * {r}.{j}" for i in [1, 2, 3] for j in [1, 2, 3]],
    )
    resf = create_expr(
        "residual_deformation", [f"{res_z}.{i} + {res_c}.{i} + {res_r}.{i}" for i in range(1, 10)]
    )
    resf.add_expr_deps(res_z, res_c, res_r, longitudinal_stretch, offaxis_compression)
    resf.add_var_deps(z, c, r)
    res_var = create_variable("ResF", solid.variables["Displacement"].get_top(), 9, freq=1)
    res_var.add_setting("TEMPORAL_UPDATE_EXPR", resf)
    return {"ResidualF": res_var}


def _create_residual_strain_vectors[T](
    mesh: MeshDefN[T], solid: SolidProblem, strain: float
) -> ResidualStrainArgs:
    top = solid.variables["Displacement"].get_top()
    z = create_variable("Z", top, 3, data=mesh["home"] / mesh["fields"]["Z"], freq=1)
    c = create_variable("C", top, 3, data=mesh["home"] / mesh["fields"]["C"], freq=1)
    r = create_variable("R", top, 3, data=mesh["home"] / mesh["fields"]["R"], freq=1)
    longitudinal_stretch = create_expr("axial_stretch", [f"1.0 + {strain}*min(t, 1.0)"])
    offaxis_compression = create_expr(
        "offaxis_compression", [f"1.0 / sqrt({longitudinal_stretch})"]
    )
    res_weights = create_expr(
        "residual_weights", [longitudinal_stretch, offaxis_compression, offaxis_compression]
    )
    res_weights.add_expr_deps(longitudinal_stretch, offaxis_compression)
    res_vectors = create_expr(
        "residual_vectors", [f"{v}.{i}" for v in [z, c, r] for i in [1, 2, 3]]
    )
    res_vectors.add_var_deps(z, c, r)
    res_var_weights = create_variable("ResWeights", top, 3, freq=1)
    res_var_weights.add_setting("TEMPORAL_UPDATE_EXPR", res_weights)
    res_var_vectors = create_variable("ResVectors", top, 9, freq=1)
    res_var_vectors.add_setting("INIT_EXPR", res_vectors)
    return {"ResidualF-weights": res_var_weights, "ResidualF-vectors": res_var_vectors}


def _create_residual_strain_deformedvectors[T](
    mesh: MeshDefN[T], solid: SolidProblem, strain: float
) -> ResidualStrainArgs:
    top = solid.variables["Displacement"].get_top()
    z = create_variable("Z", top, 3, data=mesh["home"] / mesh["fields"]["Z"], freq=1)
    c = create_variable("C", top, 3, data=mesh["home"] / mesh["fields"]["C"], freq=1)
    r = create_variable("R", top, 3, data=mesh["home"] / mesh["fields"]["R"], freq=1)
    longitudinal_stretch = create_expr("axial_stretch", [f"1.0 + {strain}*min(t, 1.0)"])
    offaxis_compression = create_expr(
        "offaxis_compression", [f"1.0 / sqrt({longitudinal_stretch})"]
    )
    res_weights = create_expr(
        "residual_weights", [longitudinal_stretch, offaxis_compression, offaxis_compression]
    )
    res_weights.add_expr_deps(longitudinal_stretch, offaxis_compression)
    res_vectors = create_expr(
        "residual_vectors", [f"{v}.{i}" for v in [z, c, r] for i in [1, 2, 3]]
    )
    res_vectors.add_var_deps(z, c, r)
    res_var_weights = create_variable("ResWeights", top, 3, freq=1)
    res_var_weights.add_setting("TEMPORAL_UPDATE_EXPR", res_weights)
    res_var_vectors = create_variable("ResVectors", top, 9, freq=1)
    res_var_vectors.add_setting("TEMPORAL_UPDATE_EXPR", res_vectors)
    return {"ResidualF-weights": res_var_weights, "ResidualF-deformedvectors": res_var_vectors}


def create_residual_strain_variables(
    prob: ProblemDef,
    solid: SolidProblem,
) -> ResidualStrainArgs | None:
    match prob.get("res_strain"):
        case {"mode": "tensor", "strain": strain}:
            return _create_residual_strain_tensor(prob["mesh"], solid, strain)
        case {"mode": "vector", "strain": strain}:
            return _create_residual_strain_vectors(prob["mesh"], solid, strain)
        case {"mode": "deformed-vector", "strain": strain}:
            return _create_residual_strain_deformedvectors(prob["mesh"], solid, strain)
        case _:
            return None


def create_solid_problem(
    prob: ProblemDef,
    v: Variables,
    bcs: Sequence[IBCPatch],
) -> SolidProblem:
    match prob.get("mode") or "forward":
        case "forward":
            mp = create_solid_mechanics_problem(f"Solid{v.U}", "QUASI_STATIC", v.Xi, v.U, pres=v.P)
        case "inverse":
            mp = create_solid_mechanics_problem(f"Solid{v.U}", "QUASI_STATIC", v.X0, v.U, pres=v.P)
            mp.set_flags("Inverse-mechanics")
    matlaws = [create_matlaw(m) for m in prob["models"]]
    mp.add_matlaw(*matlaws)
    rho = 1.06e-6
    mp.use_option("Density", rho)
    match create_residual_strain_variables(prob, mp):
        case Mapping() as strain:
            mp.add_residual_strain(strain)
        case None:
            pass
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
