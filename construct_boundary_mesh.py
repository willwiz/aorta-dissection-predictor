from pathlib import Path
from typing import TYPE_CHECKING, TypeGuard

import numpy as np
from cheartpy.elem_interfaces import get_vtk_boundary_element
from cheartpy.io import chread_d, chwrite_d_utf
from cheartpy.mesh import CheartMesh, CheartMeshSpace, CheartMeshTopology, import_cheart_mesh
from cheartpy.mesh_tools.surface_core import (
    compute_surface_normal,
    create_mesh_from_surface,
    normalize_by_row,
)
from pytools.logging import get_logger
from pytools.math import householder_orthogonal_basis
from pytools.result import Ok, Result

from data.mesh import MIA_MESH

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from cheartpy.fe.aliases import EmbbededTopologyDef, TopologyDef
    from code_pkg.components import TopologyType
    from code_pkg.mesh import MeshDefN
    from pytools.arrays import A1, A2


def is_cutplane[T](top: TopologyDef[T]) -> TypeGuard[EmbbededTopologyDef[T]]:
    match top:
        case {"master": _, "bnd": _, "mesh": _}:
            return True
        case _:
            return False


def find_cutplane_master[T](*tops: EmbbededTopologyDef[T]) -> T:
    master_to_cutplane = {t["master"]: t for t in tops}
    match len(master_to_cutplane):
        case 1: ...  # fmt: skip
        case 0:
            msg = "No cutplane found"
            raise ValueError(msg)
        case _:
            msg = f"Multiple cutplanes found: {list(master_to_cutplane.keys())}"
            raise ValueError(msg)
    return master_to_cutplane.popitem()[0]


def compute_householder_basis[F: np.floating](normals: A2[F]) -> A2[F]:
    mean_normal = normals.mean(axis=0)
    basis = householder_orthogonal_basis(mean_normal)
    return np.full((normals.shape[0], 9), basis.flatten())


def compute_zrc_basis[F: np.floating](space: A2[F], normals: A2[F]) -> A2[F]:
    centroid = space.mean(axis=0)
    mean_normal = normals.mean(axis=0)
    mean_normal = mean_normal / np.linalg.norm(mean_normal)
    z = np.full((normals.shape[0], 9), mean_normal)
    r = space - centroid
    r = r - np.einsum("ij,j,k->ik", r, mean_normal, mean_normal)
    r = normalize_by_row(r)
    c = np.cross(z, r)
    return np.concatenate((z, r, c), axis=1).astype(space.dtype)


def merge_meshes[F: np.floating, I: np.integer](
    meshes: Sequence[CheartMesh[F, I]], vs: Mapping[str, Sequence[A2[F]]]
) -> Result[tuple[CheartMesh[F, I], CheartMesh[F, I], Mapping[str, A2[F]]]]:
    ftype = meshes[0].space.v.dtype
    dtype = meshes[0].top.v.dtype
    mesh_sizes = [0] + [int(m.space.n) for m in meshes]
    node_offset: A1[I] = np.add.accumulate(mesh_sizes)
    merged_space = np.zeros((node_offset[-1], 3), dtype=ftype)
    for m, offset in zip(meshes, node_offset, strict=False):
        merged_space[offset : offset + m.space.n] = m.space.v
    tops: list[A2[I]] = [
        (m.top.v + offset).astype(dtype) for m, offset in zip(meshes, node_offset, strict=False)
    ]
    merged_top = np.concatenate(tops, axis=0)
    merged_mesh = CheartMesh(
        space=CheartMeshSpace(n=node_offset[-1], v=merged_space),
        top=CheartMeshTopology(n=len(merged_top), v=merged_top, TYPE=meshes[0].top.TYPE),
        bnd=None,
    )

    interface_space = CheartMeshSpace(
        n=len(meshes), v=np.arange(len(meshes), dtype=ftype).reshape(-1, 1)
    )
    elem_map = [np.ones((m.top.n, 1), dtype=dtype) * i for i, m in enumerate(meshes)]
    interface_mesh = CheartMesh(
        space=interface_space,
        top=CheartMeshTopology(
            n=sum(m.top.n for m in meshes),
            v=np.concatenate(elem_map, axis=0).astype(dtype),
            TYPE=meshes[0].top.TYPE,
        ),
        bnd=None,
    )
    return Ok((merged_mesh, interface_mesh, {k: np.concatenate(v, axis=0) for k, v in vs.items()}))


def make_cutplane_topology(
    defn: MeshDefN[TopologyType], planes: Sequence[TopologyType], new_home: Path, prefix: str
) -> None:
    get_logger(level="INFO")
    new_home.mkdir(parents=True, exist_ok=True)
    cutplanes = {
        k: t
        for k, t in zip(
            planes,
            [defn["top"][name] for name in planes if name in defn["top"]],
            strict=True,
        )
        if is_cutplane(t)
    }
    master = find_cutplane_master(*cutplanes.values())
    master_mesh = import_cheart_mesh(defn["top"][master]["mesh"]).unwrap()
    master_mesh.save(new_home / "Lin")
    if master_mesh.bnd is None:
        msg = f"Master mesh {master} has no boundary"
        raise ValueError(msg)
    bnd_type = get_vtk_boundary_element(master_mesh.bnd.TYPE)
    if bnd_type is None:
        msg = f"Unsupported boundary type {master_mesh.bnd.TYPE}"
        raise ValueError(msg)
    bnd_meshes = {
        k: create_mesh_from_surface(master_mesh, pln["bnd"]).unwrap()
        for k, pln in cutplanes.items()
    }
    bnd_normals = {
        k: compute_surface_normal(master_mesh, pln["bnd"]).unwrap() for k, pln in cutplanes.items()
    }
    bnd_bases = {k: compute_householder_basis(normals) for k, normals in bnd_normals.items()}
    bnd_zrc_bases = {k: compute_zrc_basis(bnd_meshes[k].space.v, bnd_normals[k]) for k in cutplanes}
    ids = {k: pln["bnd"] * np.ones((bnd_meshes[k].space.n, 1)) for k, pln in cutplanes.items()}
    merged_mesh, interface_mesh, vs = merge_meshes(
        list(bnd_meshes.values()),
        {
            "Normal": list(bnd_normals.values()),
            "Basis": list(bnd_bases.values()),
            "IDs": list(ids.values()),
            "ZRC": list(bnd_zrc_bases.values()),
        },
    ).unwrap()
    merged_mesh.save(new_home / f"{prefix}Planes")
    interface_mesh.save(new_home / f"{prefix}Interface")
    for k, v in vs.items():
        chwrite_d_utf(new_home / f"{prefix}Planes{k}-0.D", v)


def prep_fiber_directions(defn: MeshDefN[TopologyType], new_home: Path) -> None:
    a_z = chread_d(defn["home"] / "Az-1.D")
    a_r = chread_d(defn["home"] / "Ar-1.D")
    vector_z = chread_d(defn["home"] / "VectorZ-1.D")
    vector_r = chread_d(defn["home"] / "VectorR-1.D")
    z = normalize_by_row(vector_z)
    c = normalize_by_row(vector_r)
    c = c - np.einsum("ij,ij,ik->ik", c, z, z)
    c = normalize_by_row(c)
    r = np.cross(z, c)
    chwrite_d_utf(new_home / "Az-0.D", a_z)
    chwrite_d_utf(new_home / "Ar-0.D", a_r)
    chwrite_d_utf(new_home / "Z-0.D", z)
    chwrite_d_utf(new_home / "C-0.D", c)
    chwrite_d_utf(new_home / "R-0.D", r)


if __name__ == "__main__":
    branches: Sequence[TopologyType] = ["Brachial", "Carotid", "Subclavian"]
    trunk: Sequence[TopologyType] = ["Inlet", "Outlet"]
    make_cutplane_topology(MIA_MESH, branches, Path("mesh_aorta"), "Branch")
    make_cutplane_topology(MIA_MESH, trunk, Path("mesh_aorta"), "Trunk")
    prep_fiber_directions(MIA_MESH, Path("mesh_aorta"))
