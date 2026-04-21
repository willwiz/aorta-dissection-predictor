from typing import TYPE_CHECKING, NamedTuple

import numpy as np
from cheartpy.io.api import chwrite_d_utf
from cheartpy.mesh_tools.cylinder_core import create_cylinder_mesh
from cheartpy.mesh_tools.surface_core import normalize_by_row

if TYPE_CHECKING:
    from cheartpy.mesh import CheartMesh
    from pytools.arrays import A2, ToFloat

    from code_pkg.components import TopologyType

    from ._types import CylinderDef, MeshDefN


class MeshTuple[F: np.floating, I: np.integer](NamedTuple):
    disp: CheartMesh[F, I]
    lin: CheartMesh[F, I]


class MeshFields[F: np.floating](NamedTuple):
    cl: A2[F]
    center: A2[F]
    fiber: A2[F]
    normal: A2[F]


def create_fiber_field[F: np.floating, I: np.integer](
    mesh: MeshTuple[F, I], fields: MeshFields[F], *, warp: bool = False
) -> tuple[A2[F], A2[F]]:
    normal = mesh.disp.space.v - fields.center
    normal = normalize_by_row(normal)
    r = normal
    z = np.zeros_like(normal)
    if warp:
        q = 0.5 * np.pi * fields.cl[:, 0]
        z[:, 0] = np.cos(q)
        z[:, 2] = -np.sin(q)
    else:
        z[:, 0] = 1.0
    c = np.cross(r, z)
    return np.column_stack((z, c, r)).astype(fields.cl.dtype), normal.astype(fields.cl.dtype)


def warp_in_y[F: np.floating](x: A2[F]) -> A2[F]:
    c = np.zeros_like(x)
    radius = 2.0 * x[:, 0].max() / np.pi
    q = 0.5 * np.pi * (1.0 - x[:, 0] / x[:, 0].max())
    r = radius + x[:, 2]
    c[:, 0] = r * np.cos(q)
    c[:, 1] = x[:, 1]
    c[:, 2] = r * np.sin(q)
    return c


def define_centerline_field[F: np.floating, I: np.integer](
    mesh: CheartMesh[F, I],
) -> A2[F]:
    center_line = mesh.space.v[:, [0]] / mesh.space.v[:, 0].max()
    x = mesh.space.v[:, 2]
    circval = (x - x.min()) / (x.max() - x.min())
    return np.hstack((center_line, circval[:, None]))


def create_center_pos[F: np.floating, I: np.integer](mesh: CheartMesh[F, I], cl: A2[F]) -> A2[F]:
    center = np.zeros_like(mesh.space.v)
    center[:, 0] = mesh.space.v[:, 0].max() * cl[:, 0]
    return center


def create_cylinder_mesh_tuple(
    geo: CylinderDef,
    *,
    quad: bool,
) -> tuple[MeshTuple[np.float64, np.intc], MeshFields[np.float64]]:
    shape: tuple[ToFloat, ToFloat, ToFloat, ToFloat] = (
        *geo["shape"],
        geo.get("offset", 0.0),
    )
    dim = geo["size"]
    lin_mesh, quad_mesh = create_cylinder_mesh(shape, dim, "x", make_quad=quad)
    disp_mesh = quad_mesh or lin_mesh
    cl = define_centerline_field(disp_mesh)
    center = create_center_pos(disp_mesh, cl)
    if geo.get("warp"):
        lin_mesh.space.v = warp_in_y(lin_mesh.space.v)
        disp_mesh.space.v = warp_in_y(disp_mesh.space.v)
        center = warp_in_y(center)
    return MeshTuple(disp_mesh, lin_mesh), MeshFields(
        cl, center, np.zeros_like(cl), np.zeros_like(cl)
    )


def make_cylinder_mesh(
    geo: CylinderDef, *, quad: bool
) -> tuple[MeshTuple[np.float64, np.intc], MeshFields[np.float64]]:
    mesh, fields = create_cylinder_mesh_tuple(geo, quad=quad)
    fiber, normal = create_fiber_field(mesh, fields, warp=geo.get("warp", False))
    return mesh, MeshFields(fields.cl, fields.center, fiber, normal)


def export_cylinder_mesh[F: np.floating, I: np.integer](
    param: MeshDefN[TopologyType], mesh: MeshTuple[F, I], fields: MeshFields[F] | None
) -> None:
    param["home"].mkdir(parents=True, exist_ok=True)
    param["top"]["Pres"]["mesh"].parent.mkdir(parents=True, exist_ok=True)
    param["top"]["Disp"]["mesh"].parent.mkdir(parents=True, exist_ok=True)
    mesh.lin.save(param["home"] / param["top"]["Pres"]["mesh"])
    mesh.disp.save(param["home"] / param["top"]["Disp"]["mesh"])
    if not fields:
        return
    field_list = (
        (param["fields"]["a_z"], fields.cl),
        (param["fields"]["normal"], fields.normal),
        (param["fields"]["fiber"], fields.fiber),
        ("Z-0.D", fields.fiber[:, 0:3]),
        ("C-0.D", fields.fiber[:, 3:6]),
        ("R-0.D", fields.fiber[:, 6:9]),
    )
    for name, field in field_list:
        chwrite_d_utf(param["home"] / name, field)
