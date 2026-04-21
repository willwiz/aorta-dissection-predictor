from typing import TYPE_CHECKING

from code_pkg.mesh import MeshDefN, export_cylinder_mesh, make_cylinder_mesh

from data.mesh import NEW_CYLINDER

if TYPE_CHECKING:
    from code_pkg.components import TopologyType

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


if __name__ == "__main__":
    make_mesh(NEW_CYLINDER)
