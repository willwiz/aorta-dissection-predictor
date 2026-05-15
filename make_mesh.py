from typing import TYPE_CHECKING

from cheartpy.cl.mesh import create_centerline_topology_in_surf, export_cl_mesh
from cheartpy.io import chread_d
from cheartpy.mesh import import_cheart_mesh
from code_pkg.mesh import MeshDefN, TopologyType, export_cylinder_mesh, make_cylinder_mesh

from data.mesh import NEW_CYLINDER

if TYPE_CHECKING:
    import numpy as np
    from cheartpy.cl.types import CLDef

_QUAD_ORDER = 2


def make_mesh(mesh: MeshDefN[TopologyType]) -> None:
    order = mesh["top"]["Disp"].get("order")
    if not order:
        msg = "Mesh order not specified"
        raise ValueError(msg)
    geo = mesh["geo"]
    match geo:
        case {"size": _}: ...  # fmt: skip
        case _:
            print(f"Unsupported geometry: {geo}")
            raise SystemExit(1)
    _mesh, _fields = make_cylinder_mesh(geo, quad=(order == _QUAD_ORDER))
    export_cylinder_mesh(mesh, _mesh, _fields)


def create_cl_mesh(defn: MeshDefN[TopologyType], n: int) -> None:
    mesh = import_cheart_mesh(defn["top"]["Disp"]["mesh"]).unwrap()
    az_field = chread_d(defn["home"] / defn["fields"]["a_z"])[:, 0]
    cl_def: CLDef[np.float64] = {
        "home": defn["home"],
        "a_z": az_field,
        "n": n,
        "prefix": {"prefix": "CL"},
    }
    dl_def: CLDef[np.float64] = {
        "home": defn["home"],
        "a_z": az_field,
        "n": 8,
        "prefix": {"prefix": "DL"},
    }
    match defn["top"]["Outer"]:
        case {"bnd": bnd}: ...  # fmt: skip
        case _:
            print("Boundary definition for mesh is wrong")
            raise SystemExit(1)
    cl = create_centerline_topology_in_surf(mesh, bnd, cl_def, no_boundary=True).unwrap()
    export_cl_mesh(cl, cl_def)
    dl = create_centerline_topology_in_surf(mesh, bnd, dl_def).unwrap()
    export_cl_mesh(dl, dl_def)


if __name__ == "__main__":
    make_mesh(NEW_CYLINDER)
    create_cl_mesh(NEW_CYLINDER, n=16)
