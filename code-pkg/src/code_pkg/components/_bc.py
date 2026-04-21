from typing import TYPE_CHECKING, Literal

from cheartpy.fe.api import create_bcpatch, create_expr, create_time_scheme
from cheartpy.fe.physics.api import create_rotation_constraint

if TYPE_CHECKING:
    from collections.abc import Sequence

    from cheartpy.fe.trait import IBCPatch, IProblem, ITimeScheme, IVariable

    from code_pkg.mesh import MeshDefN

    from ._types import (
        BCDef,
        LinearPressure,
        PressureDef,
        TimeDef,
        TopologyMap,
        TopologyType,
        Variables,
    )


def create_time(time: TimeDef) -> ITimeScheme:
    return create_time_scheme("time", time.get("start", 1), time["end"], time["step"])


def _create_linear_pressure_curve(tag: int, v: IVariable, pres: LinearPressure) -> IBCPatch:
    curve = create_expr(
        "pressure_curve",
        [f"{-pres['amp']} * min((t - 1.0)/{pres['duration']}, 1.0) * (t > 1.0)"],
    )
    return create_bcpatch(tag, v, "scaled_normal", curve)


def create_pressure_curve(tag: int, v: IVariable, pres: PressureDef) -> IBCPatch:
    match pres:
        case {"mode": "linear"}:
            return _create_linear_pressure_curve(tag, v, pres)


def create_slip_bc(
    mesh: MeshDefN[TopologyType],
    top: TopologyMap[TopologyType],
    svars: Variables,
    params: tuple[Literal["Inlet", "Outlet"], Literal["x", "y", "z"]],
) -> tuple[Sequence[IBCPatch], Sequence[IProblem]]:
    surf, orientation = params
    component = {"x": 1, "y": 2, "z": 3}[orientation]
    patchs = [create_bcpatch(mesh["bnds"][surf]["tag"], (svars.U, component), "dirichlet", 0.0)]
    constraints = create_rotation_constraint(
        surf, top[surf], {"R": {orientation}}, space=svars.Xi, disp=svars.U, freq=-1
    )
    return patchs, [constraints]


def create_noslip_bc(
    mesh: MeshDefN[TopologyType],
    svars: Variables,
    params: tuple[Literal["Inlet", "Outlet"], Literal["x", "y", "z"]],
) -> tuple[Sequence[IBCPatch], Sequence[IProblem]]:
    surf, _ = params
    patchs = [create_bcpatch(mesh["bnds"][surf]["tag"], svars.U, "dirichlet", 0.0, 0.0, 0.0)]
    return patchs, []


def create_patch(
    mesh: MeshDefN[TopologyType],
    top: TopologyMap[TopologyType],
    svars: Variables,
    mode: Literal["SLIP", "HOLD"],
    params: tuple[Literal["Inlet", "Outlet"], Literal["x", "y", "z"]],
) -> tuple[Sequence[IBCPatch], Sequence[IProblem]]:
    match mode:
        case "SLIP":
            return create_slip_bc(mesh, top, svars, params)
        case "HOLD":
            return create_noslip_bc(mesh, svars, params)


def create_boundary_conditions(
    mesh: MeshDefN[TopologyType], top: TopologyMap[TopologyType], svars: Variables, bc: BCDef
) -> tuple[Sequence[IBCPatch], Sequence[IProblem]]:
    pres = create_pressure_curve(mesh["bnds"]["Inner"]["tag"], svars.U, bc["Pres"])
    inlet = create_patch(mesh, top, svars, bc.get("Inlet", "SLIP"), ("Inlet", "x"))
    outlet = create_patch(mesh, top, svars, bc.get("Outlet", "SLIP"), ("Outlet", "x"))
    return [pres, *inlet[0], *outlet[0]], [*inlet[1], *outlet[1]]
