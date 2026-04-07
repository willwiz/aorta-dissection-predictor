from code_pkg.mesh import MeshDef, export_cylinder_mesh, make_cylinder_mesh

from data.mesh import DEFAULT_CYLINDER

_QUAD_ORDER = 2


def make_mesh(mesh: MeshDef) -> None:
    _mesh, _fields = make_cylinder_mesh(
        mesh["geo"], quad=(mesh["top"]["Disp"]["order"] == _QUAD_ORDER)
    )
    export_cylinder_mesh(mesh, _mesh, _fields)


if __name__ == "__main__":
    make_mesh(DEFAULT_CYLINDER)
