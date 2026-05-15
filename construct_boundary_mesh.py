from typing import TYPE_CHECKING, LiteralString, TypeGuard, TypeIs

import numpy as np
from cheartpy.cl.mesh import (
    compute_a_c_coordinate,
    create_centerline_topology_in_surf,
    export_cl_mesh,
)
from cheartpy.elem_interfaces import get_vtk_boundary_element
from cheartpy.io import chread_d, chwrite_d_utf
from cheartpy.mesh import CheartMesh, CheartMeshSpace, CheartMeshTopology, import_cheart_mesh
from cheartpy.mesh_tools.surface_core import (
    compute_surface_normal,
    create_mesh_from_surface,
    normalize_by_row,
)
from code_pkg.mesh import MeshDefN
from pytools.logging import get_logger
from pytools.math import householder_orthogonal_basis
from pytools.result import Err, Ok, Result

from data.mesh import AORTA_MESH

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path

    from cheartpy.cl.types import CLDef
    from cheartpy.fe.aliases import EmbbededTopologyDef, TopologyDef
    from code_pkg.mesh import DissectedType, MeshDefN, TopologyType
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
    z = np.full((normals.shape[0], 3), mean_normal)
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


def make_cutplane_topology[T: TopologyType | DissectedType](
    defn: MeshDefN[T],
    planes: Sequence[T],
    new_home: Path,
    prefix: str,
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


def prep_fiber_directions[F: np.floating, I: np.integer](
    mesh: CheartMesh[F, I],
    defn: MeshDefN[TopologyType] | MeshDefN[DissectedType],
    new_home: Path,
    width: float = 0.005,
) -> None:
    dtype = mesh.space.v.dtype
    a_z = chread_d(defn["home"] / "Az-1.D", dtype=dtype)[:, 0]
    a_r = chread_d(defn["home"] / "Ar-1.D")
    vector_z = chread_d(defn["home"] / "VectorZ-1.D", dtype=dtype)
    vector_r = chread_d(defn["home"] / "VectorR-1.D")
    z = normalize_by_row(vector_z)
    r = normalize_by_row(vector_r)
    r = r - np.einsum("ij,ij,ik->ik", r, z, z)
    r = normalize_by_row(r)
    c = np.cross(r, z)
    a_c = compute_a_c_coordinate(mesh, a_z=a_z, v_z=z, width=width)
    chwrite_d_utf(new_home / defn["fields"]["a_z"], a_z)
    chwrite_d_utf(new_home / defn["fields"]["a_r"], a_r)
    chwrite_d_utf(new_home / defn["fields"]["a_c"], a_c)
    chwrite_d_utf(new_home / defn["fields"]["Z"], z)
    chwrite_d_utf(new_home / defn["fields"]["C"], c)
    chwrite_d_utf(new_home / defn["fields"]["R"], r)


def is_top_name[T: LiteralString](name: str, top: Mapping[T, TopologyDef[T]]) -> TypeIs[T]:
    return name in top


def get_embedding_id[T: LiteralString](
    top: Mapping[T, TopologyDef[T]], top_name: str
) -> Result[tuple[T, int]]:
    if not is_top_name(top_name, top):
        msg = f"Topology {top_name} not found in mesh definition"
        return Err(ValueError(msg))
    match top[top_name]:
        case {"bnd": bnd, "master": master}:
            return Ok((master, bnd))
        case _:
            msg = f"Topology {top_name} is not an embedded topology"
            return Err(ValueError(msg))


def create_cl_mesh[T: TopologyType | DissectedType](defn: MeshDefN[T], n: int) -> None:
    match get_embedding_id(defn["top"], "Outer"):
        case Ok((master, bnd)): ...  # fmt: skip
        case Err(e):
            print(e)
            raise SystemExit(1)
    mesh = import_cheart_mesh(defn["top"][master]["mesh"]).unwrap()
    az_field = chread_d(defn["home"] / defn["fields"]["a_z"])[:, 0]
    cl_def: CLDef[np.float64] = {
        "home": defn["home"],
        "a_z": az_field,
        "n": n,
        "prefix": {"prefix": "CL"},
    }
    cl = create_centerline_topology_in_surf(mesh, bnd, cl_def, no_boundary=True).unwrap()
    dl_def: CLDef[np.float64] = {
        "home": defn["home"],
        "a_z": az_field,
        "n": 5,
        "prefix": {"prefix": "DL"},
    }
    export_cl_mesh(cl, cl_def)
    match get_embedding_id(defn["top"], "Outer"):
        case Ok((master, bnd)): ...  # fmt: skip
        case Err(e):
            print(e)
            raise SystemExit(1)
    dl = create_centerline_topology_in_surf(mesh, bnd, dl_def).unwrap()
    export_cl_mesh(dl, dl_def)


if __name__ == "__main__":
    # branches: Sequence[DissectedType] = ["Brachial", "Carotid", "Subclavian", "ca1", "ca2"]
    # trunk: Sequence[TopologyType] = ["Inlet", "Outlet"]
    # make_cutplane_topology(DISSECTION_MESH, branches, Path("mesh_aorta"), "Branch")
    # make_cutplane_topology(DISSECTION_MESH, trunk, Path("mesh_aorta"), "Trunk")
    # create_cl_mesh(DISSECTION_MESH, n=16)
    branches: Sequence[TopologyType] = ["Brachial", "Carotid", "Subclavian"]
    trunk: Sequence[TopologyType] = ["Outlet"]
    mesh = import_cheart_mesh(AORTA_MESH["top"]["Pres"]["mesh"]).unwrap()
    make_cutplane_topology(AORTA_MESH, branches, AORTA_MESH["home"], "Branch")
    make_cutplane_topology(AORTA_MESH, trunk, AORTA_MESH["home"], "Trunk")
    prep_fiber_directions(mesh, AORTA_MESH, AORTA_MESH["home"])
    create_cl_mesh(AORTA_MESH, n=64)
