from code_pkg.mesh import export_cylinder_mesh, make_cylinder_mesh

from data.mesh import DEFAULT_CYLINDER

_QUAD_ORDER = 2


def make_mesh() -> None:
    mesh, fields = make_cylinder_mesh(
        DEFAULT_CYLINDER["geo"], quad=(DEFAULT_CYLINDER["top"]["Disp"]["order"] == _QUAD_ORDER)
    )
    export_cylinder_mesh(DEFAULT_CYLINDER, mesh, fields)


if __name__ == "__main__":
    make_mesh()
